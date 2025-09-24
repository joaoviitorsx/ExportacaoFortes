import queue
import threading
import pandas as pd

from src.repositories.registrosFS.registro0000Repository import Registro0000Repository
from src.repositories.registrosFS.registro0150Repository import Registro0150Repository
from src.repositories.registrosFS.registro0200Repository import Registro0200Repository
from src.repositories.registrosFS.registroC100Repository import RegistroC100Repository
from src.repositories.registrosFS.registroC170Repository import RegistroC170Repository
from src.repositories.registrosFS.registroC190Repository import RegistroC190Repository

class Persistencia(threading.Thread):
    def __init__(self, fila: queue.PriorityQueue, session, empresa_id, buffer_size=10000):
        super().__init__()
        self.fila = fila
        self.session = session
        self.empresa_id = empresa_id
        self.daemon = True
        self.buffer_size = buffer_size

        self.repo0000 = Registro0000Repository(session)
        self.repo0150 = Registro0150Repository(session)
        self.repo0200 = Registro0200Repository(session)
        self.repoC100 = RegistroC100Repository(session)
        self.repoC170 = RegistroC170Repository(session)
        self.repoC190 = RegistroC190Repository(session)

        self.mapa_documentos = {}
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

    def salvarRegistro0150(self, dados):
        print(f"[INFO] Salvando 0150 ({len(dados)})")
        self.repo0150.salvamento(dados)

    def salvarRegistro0200(self, dados):
        print(f"[INFO] Salvando 0200 ({len(dados)})")
        self.repo0200.salvamento(dados)

    def salvarRegistroC100(self, dados):
        print(f"[INFO] Salvando C100 ({len(dados)})")
        self.repoC100.salvamento(dados)

        if dados:
            periodo = dados[0].get("periodo")
            empresa_id = dados[0].get("empresa_id")

            rows = self.repoC100.buscarIDS(periodo, empresa_id)
            for row in rows:  
                num_doc = str(row["num_doc"]).zfill(9)
                self.mapa_documentos[num_doc] = {
                    "id_c100": row["id"],
                    "ind_oper": row["ind_oper"],
                    "cod_part": row["cod_part"],
                    "chv_nfe": row["chv_nfe"],
                    "periodo": periodo,
                    "empresa_id": empresa_id,
                }

    def salvarRegistroC170(self, dados):
        print(f"[INFO] Salvando C170 ({len(dados)})")
        for registro in dados:
            num_doc = str(registro.get("num_doc", "")).zfill(9)
            doc_info = self.mapa_documentos.get(num_doc)

            if doc_info:
                registro.setdefault("c100_id", doc_info.get("id_c100"))
                registro.setdefault("periodo", doc_info.get("periodo"))
                registro.setdefault("empresa_id", doc_info.get("empresa_id"))

        self.repoC170.salvamento(dados)

    def salvarRegistroC190(self, dados):
        print(f"[INFO] Salvando C190 ({len(dados)})")
        for registro in dados:
            num_doc = str(registro.get("num_doc", "")).zfill(9)
            doc_info = self.mapa_documentos.get(num_doc)

            if doc_info:
                registro.setdefault("c100_id", doc_info.get("id_c100"))
                registro.setdefault("ind_oper", doc_info.get("ind_oper"))
                registro.setdefault("cod_part", doc_info.get("cod_part"))
                registro.setdefault("chv_nfe", doc_info.get("chv_nfe"))
                registro.setdefault("periodo", doc_info.get("periodo"))
                registro.setdefault("empresa_id", doc_info.get("empresa_id"))

        self.repoC190.salvamento(dados)
