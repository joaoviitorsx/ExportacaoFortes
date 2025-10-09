import queue
import threading
import pandas as pd

from ...repositories.registrosRepo.registro0000Repository import Registro0000Repository
from ...repositories.registrosRepo.registro0150Repository import Registro0150Repository
from ...repositories.registrosRepo.registro0200Repository import Registro0200Repository
from ...repositories.registrosRepo.registroC100Repository import RegistroC100Repository
from ...repositories.registrosRepo.registroC170Repository import RegistroC170Repository
from ...repositories.registrosRepo.registroC190Repository import RegistroC190Repository

class Persistencia(threading.Thread):
    #compartilhado entre todas as threads
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

        self.prioridades = {
            "0000": 1,
            "0150": 2,
            "0200": 3,
            "C100": 4,
            "C170": 5,
            "C190": 6,
        }

    def run(self):
        try:
            while True:
                lote = self.fila.get()
                prioridade, tipo, contador, dados = lote

                if tipo == "parou":
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

                self.fila.task_done()
        finally:
            self.session.close()

    def salvarRegistro0000(self, dados):
        print(f"[INFO] Salvando 0000 ({len(dados)})")
        self.repo0000.salvamento(dados)
        self.session.commit()

        Persistencia.eventC100Finish.clear()
        with Persistencia.mapa_lock:
            Persistencia.mapa_documentos.clear()

    def salvarRegistro0150(self, dados):
        print(f"[INFO] Salvando 0150 ({len(dados)})")
        self.repo0150.salvamento(dados)
        self.session.commit()

    def salvarRegistro0200(self, dados):
        print(f"[INFO] Salvando 0200 ({len(dados)})")
        self.repo0200.salvamento(dados)
        self.session.commit()

    def salvarRegistroC100(self, dados):
        print(f"[INFO] Salvando C100 ({len(dados)})")
        self.repoC100.salvamento(dados)
        self.session.commit()

        if not dados:
            return

        periodo = dados[0].get("periodo")
        empresa_id = dados[0].get("empresa_id")

        rows = self.repoC100.buscarIDS(periodo, empresa_id)
        with Persistencia.mapa_lock:
            for row in rows:
                num_doc = str(row["num_doc"]).zfill(9)
                Persistencia.mapa_documentos[num_doc] = {
                    "id_c100": row["id"],
                    "ind_oper": row.get("ind_oper"),
                    "cod_part": row.get("cod_part"),
                    "chv_nfe": row.get("chv_nfe"),
                    "periodo": periodo,
                    "empresa_id": empresa_id,
                }
            print(f"[INFO] Mapa de documentos atualizado ({len(Persistencia.mapa_documentos)} docs).")

        Persistencia.eventC100Finish.set()

    def salvarRegistroC170(self, dados):
        print(f"[INFO] Salvando C170 ({len(dados)})")
        Persistencia.eventC100Finish.wait()

        with Persistencia.mapa_lock:
            for registro in dados:
                num_doc = str(registro.get("num_doc", "")).zfill(9)
                doc_info = Persistencia.mapa_documentos.get(num_doc)
                if doc_info:
                    registro["c100_id"]   = doc_info["id_c100"]
                    registro["periodo"]   = doc_info["periodo"]
                    registro["empresa_id"]= doc_info["empresa_id"]
                else:
                    print(f"[WARN] C170 sem match: num_doc={num_doc} não encontrado no mapa_documentos.")

        self.repoC170.salvamento(dados)
        self.session.commit()

    def salvarRegistroC190(self, dados):
        print(f"[INFO] Salvando C190 ({len(dados)})")
        Persistencia.eventC100Finish.wait()

        with Persistencia.mapa_lock:
            for registro in dados:
                num_doc = str(registro.get("num_doc", "")).zfill(9)
                doc_info = Persistencia.mapa_documentos.get(num_doc)
                if doc_info:
                    registro["c100_id"] = doc_info["id_c100"]
                    registro["ind_oper"] = doc_info.get("ind_oper")
                    registro["cod_part"] = doc_info.get("cod_part")
                    registro["chv_nfe"] = doc_info.get("chv_nfe")
                    registro["periodo"] = doc_info["periodo"]
                    registro["empresa_id"] = doc_info["empresa_id"]
                else:
                    print(f"[WARN] C190 sem match: num_doc={num_doc} não encontrado no mapa_documentos.")

        self.repoC190.salvamento(dados)
        self.session.commit()
