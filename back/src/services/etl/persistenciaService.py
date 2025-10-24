import queue
import threading
import pandas as pd
from collections import defaultdict

from ...repositories.registrosRepo.registro0000Repository import Registro0000Repository
from ...repositories.registrosRepo.registro0150Repository import Registro0150Repository
from ...repositories.registrosRepo.registro0200Repository import Registro0200Repository
from ...repositories.registrosRepo.registroC100Repository import RegistroC100Repository
from ...repositories.registrosRepo.registroC170Repository import RegistroC170Repository
from ...repositories.registrosRepo.registroC190Repository import RegistroC190Repository

class Persistencia(threading.Thread):
    eventC100Finish = threading.Event()
    mapa_documentos = {}
    mapa_lock = threading.Lock()

    def __init__(self, fila: queue.PriorityQueue, session, empresa_id):
        super().__init__()
        self.fila = fila
        self.session = session
        self.empresa_id = empresa_id
        self.daemon = True

        self.repo0000 = Registro0000Repository(session)
        self.repo0150 = Registro0150Repository(session)
        self.repo0200 = Registro0200Repository(session)
        self.repoC100 = RegistroC100Repository(session)
        self.repoC170 = RegistroC170Repository(session)
        self.repoC190 = RegistroC190Repository(session)

        # Buffer local para acumular antes de commitar
        self.buffer = defaultdict(list)
        self.buffer_size = 1000  # Ajustar conforme necessário
        self.commit_counter = 0

    def run(self):
        try:
            while True:
                lote = self.fila.get()
                prioridade, tipo, contador, dados = lote

                if tipo == "parou":
                    self._flush_all_buffers()  # Garante que tudo seja salvo
                    self.fila.task_done()
                    break

                try:
                    if tipo == "0000":
                        self.salvarRegistro0000(dados)
                    elif tipo == "0150":
                        self.salvarRegistro0150(dados)
                    elif tipo == "0200":
                        self.salvarRegistro0200(dados)
                    elif tipo == "C100":
                        self.salvarRegistroC100(dados)
                    elif tipo == "C170":
                        self.salvarRegistroC170(dados)
                    elif tipo == "C190":
                        self.salvarRegistroC190(dados)
                except Exception as e:
                    print(f"[ERRO] Falha ao salvar lote {tipo}: {e}")
                    self.session.rollback()

                self.fila.task_done()
        finally:
            self._flush_all_buffers()
            self.session.close()

    def _flush_all_buffers(self):
        """Força commit de todos os buffers pendentes"""
        try:
            if any(self.buffer.values()):
                print(f"[INFO] Fazendo flush final dos buffers...")
                self.session.commit()
                self.buffer.clear()
        except Exception as e:
            print(f"[ERRO] Falha ao fazer flush: {e}")
            self.session.rollback()

    def _commit_periodico(self, forca=False):
        """Commit periódico em lote para reduzir I/O"""
        self.commit_counter += 1
        if forca or self.commit_counter >= 10:  # A cada 10 operações
            try:
                self.session.commit()
                self.commit_counter = 0
            except Exception as e:
                print(f"[ERRO] Falha no commit: {e}")
                self.session.rollback()
                raise

    def salvarRegistro0000(self, dados):
        print(f"[INFO] Salvando 0000 ({len(dados)})")
        self.repo0000.salvamento(dados)
        self._commit_periodico(forca=True)  # Forçar commit em 0000

        Persistencia.eventC100Finish.clear()
        with Persistencia.mapa_lock:
            Persistencia.mapa_documentos.clear()

    def salvarRegistro0150(self, dados):
        print(f"[INFO] Salvando 0150 ({len(dados)})")
        self.repo0150.salvamento(dados)
        self._commit_periodico()

    def salvarRegistro0200(self, dados):
        print(f"[INFO] Salvando 0200 ({len(dados)})")
        self.repo0200.salvamento(dados)
        self._commit_periodico()

    def salvarRegistroC100(self, dados):
        print(f"[INFO] Salvando C100 ({len(dados)})")
        self.repoC100.salvamento(dados)
        self._commit_periodico(forca=True)  # Importante: commit antes de buscar IDs

        if not dados:
            return

        periodo = dados[0].get("periodo")
        empresa_id = dados[0].get("empresa_id")

        # Otimização: buscar apenas os IDs dos documentos recém-inseridos
        rows = self.repoC100.buscarIDS(periodo, empresa_id)
        
        # Criar mapa local primeiro, depois atualizar o global rapidamente
        mapa_local = {}
        for row in rows:
            num_doc = str(row["num_doc"]).zfill(9)
            mapa_local[num_doc] = {
                "id_c100": row["id"],
                "ind_oper": row.get("ind_oper"),
                "cod_part": row.get("cod_part"),
                "chv_nfe": row.get("chv_nfe"),
                "periodo": periodo,
                "empresa_id": empresa_id,
            }
        
        # Lock mínimo para atualizar o mapa global
        with Persistencia.mapa_lock:
            Persistencia.mapa_documentos.update(mapa_local)
            print(f"[INFO] Mapa de documentos atualizado ({len(Persistencia.mapa_documentos)} docs).")

        Persistencia.eventC100Finish.set()

    def salvarRegistroC170(self, dados):
        print(f"[INFO] Processando C170 ({len(dados)})")
        Persistencia.eventC100Finish.wait()

        # Enriquecer dados fora do lock para reduzir contenção
        dados_enriquecidos = []
        with Persistencia.mapa_lock:
            for registro in dados:
                num_doc = str(registro.get("num_doc", "")).zfill(9)
                doc_info = Persistencia.mapa_documentos.get(num_doc)
                
                registro_copia = registro.copy()
                if doc_info:
                    registro_copia["c100_id"] = doc_info["id_c100"]
                    registro_copia["periodo"] = doc_info["periodo"]
                    registro_copia["empresa_id"] = doc_info["empresa_id"]
                    dados_enriquecidos.append(registro_copia)
                else:
                    print(f"[WARN] C170 sem match: num_doc={num_doc}")

        if dados_enriquecidos:
            self.repoC170.salvamento(dados_enriquecidos)
            self._commit_periodico()

    def salvarRegistroC190(self, dados):
        print(f"[INFO] Processando C190 ({len(dados)})")
        Persistencia.eventC100Finish.wait()

        dados_enriquecidos = []
        with Persistencia.mapa_lock:
            for registro in dados:
                num_doc = str(registro.get("num_doc", "")).zfill(9)
                doc_info = Persistencia.mapa_documentos.get(num_doc)
                
                registro_copia = registro.copy()
                if doc_info:
                    registro_copia["c100_id"] = doc_info["id_c100"]
                    registro_copia["ind_oper"] = doc_info.get("ind_oper")
                    registro_copia["cod_part"] = doc_info.get("cod_part")
                    registro_copia["chv_nfe"] = doc_info.get("chv_nfe")
                    registro_copia["periodo"] = doc_info["periodo"]
                    registro_copia["empresa_id"] = doc_info["empresa_id"]
                    dados_enriquecidos.append(registro_copia)
                else:
                    print(f"[WARN] C190 sem match: num_doc={num_doc}")

        if dados_enriquecidos:
            self.repoC190.salvamento(dados_enriquecidos)
            self._commit_periodico()