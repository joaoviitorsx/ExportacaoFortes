from typing import Dict, Any
from ...repositories.registrosRepo.registro0000Repository import Registro0000Repository
from ...repositories.registrosRepo.registro0150Repository import Registro0150Repository
from ...repositories.registrosRepo.registro0190Repository import Registro0190Repository
from ...repositories.registrosRepo.registro0200Repository import Registro0200Repository
from ...repositories.registrosRepo.registro0220Repository import Registro0220Repository
from ...repositories.registrosRepo.registro0221Repository import Registro0221Repository
from ...repositories.registrosRepo.registroC100Repository import RegistroC100Repository
from ...repositories.registrosRepo.registroC170Repository import RegistroC170Repository
from ...repositories.registrosRepo.registroC190Repository import RegistroC190Repository

class PersistenciaService:
    def __init__(self, session):
        self.session = session
        self.repo0000 = Registro0000Repository(session)
        self.repo0150 = Registro0150Repository(session)
        self.repo0190 = Registro0190Repository(session)
        self.repo0200 = Registro0200Repository(session)
        self.repo0220 = Registro0220Repository(session)
        self.repo0221 = Registro0221Repository(session)
        self.repoC100 = RegistroC100Repository(session)
        self.repoC170 = RegistroC170Repository(session)
        self.repoC190 = RegistroC190Repository(session)

    #Persiste os dados extraídos do SPED, garantindo integridade entre C100, C170 e C190.
    def salvar(self, dados: Dict[str, Any]) -> Dict[str, int]:
        stats = {"0000": 0, "0150": 0, "0190": 0, "0200": 0, "0220": 0, "0221": 0, "c100": 0, "c170": 0, "c190": 0, "notas_ignoradas": 0}

        try:
            cab = dados.get("cabecalhos", {})

            if cab.get("0000"):
                self.repo0000.salvamento(cab["0000"])
                stats["0000"] = len(cab["0000"])

            if cab.get("0150"):
                self.repo0150.salvamento(cab["0150"])
                stats["0150"] = len(cab["0150"])

            if cab.get("0190"):
                self.repo0190.salvamento(cab["0190"])
                stats["0190"] = len(cab["0190"])

            if cab.get("0200"):
                self.repo0200.salvamento(cab["0200"])
                stats["0200"] = len(cab["0200"])

            if cab.get("0220"):
                self.repo0220.salvamento(cab["0220"])
                stats["0220"] = len(cab["0220"])

            if cab.get("0221"):
                self.repo0221.salvamento(cab["0221"])
                stats["0221"] = len(cab["0221"])

            self.session.commit()

            #Notas Fiscais
            lote_c100, lote_c170, lote_c190 = [], [], []

            for nota in dados["notas"]:
                if not nota["c170"]:
                    stats["notas_ignoradas"] += 1
                    continue

                lote_c100.append(nota["c100"])
                lote_c170.extend(nota["c170"])
                lote_c190.extend(nota["c190"])

            # C100
            if lote_c100:
                self.repoC100.salvamento(lote_c100)
                self.session.commit()
                stats["c100"] = len(lote_c100)

                periodo = lote_c100[0]["periodo"]
                empresa_id = lote_c100[0]["empresa_id"]
                rows = self.repoC100.buscarIDS(periodo, empresa_id)

                mapa_ids = {r["doc_key"]: r["id"] for r in rows if r.get("doc_key") and r.get("id")}

                #C170
                for c170 in lote_c170:
                    doc_key = c170.get("doc_key")
                    if doc_key in mapa_ids:
                        c170["c100_id"] = mapa_ids[doc_key]
                lote_c170_validos = [c for c in lote_c170 if c.get("c100_id")]
                if lote_c170_validos:
                    self.repoC170.salvamento(lote_c170_validos)
                    self.session.commit()
                    stats["c170"] = len(lote_c170_validos)

                #C190
                for c190 in lote_c190:
                    doc_key = c190.get("doc_key")
                    if doc_key in mapa_ids:
                        c190["c100_id"] = mapa_ids[doc_key]
                lote_c190_validos = [c for c in lote_c190 if c.get("c100_id")]
                if lote_c190_validos:
                    self.repoC190.salvamento(lote_c190_validos)
                    self.session.commit()
                    stats["c190"] = len(lote_c190_validos)

            return stats

        except Exception:
            self.session.rollback()
            raise
