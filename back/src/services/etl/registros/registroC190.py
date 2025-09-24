import pandas as pd
from src.utils.sanitizacao import parseDecimal
from src.services.etl.validadorService import ValidadorService

class RegistroC190Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.mapa_documentos = {}
        self.tabela = "registro_c190"
        self.nome = "C190"

    def set_context(self, periodo, filial=None):
        self.periodo = periodo

    def setDocumentos(self, mapa_documentos: dict):
        self.mapa_documentos = mapa_documentos

    def sanitizarPartes(self, partes: list[str]) -> list[str]:
        return (partes + [None] * (13 - len(partes)))[:13]

    def processar(self, partes: list[str], num_doc: str) -> None:
        partes = self.sanitizarPartes(partes)
        num_doc = str(num_doc).zfill(9)

        dados = {
            "empresa_id": self.empresa_id,
            "periodo": self.periodo,
            "reg": partes[0],
            "cst_icms": partes[1],
            "cfop": partes[2],
            "aliq_icms": parseDecimal(partes[3]) if partes[3] not in (None, '', ' ') else 0.00,
            "vl_opr": parseDecimal(partes[4]),
            "vl_bc_icms": parseDecimal(partes[5]),
            "vl_icms": parseDecimal(partes[6]),
            "vl_bc_icms_st": parseDecimal(partes[7]),
            "vl_icms_st": parseDecimal(partes[8]),
            "vl_red_bc": parseDecimal(partes[9]),
            "vl_ipi": parseDecimal(partes[10]),
            "cod_obs": partes[11],
            "num_doc": num_doc,   # chave de vínculo
            "ativo": True,
        }
        
        ok, erros = ValidadorService.validarRegistroC190(dados)
        if ok:
            self.lote.append(dados)
        else:
            return
        
    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
