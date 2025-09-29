import pandas as pd
from datetime import datetime
from .....src.utils.sanitizacao import parseDecimal, parseDate
from .....src.services.etl.validadorService import ValidadorService

class RegistroC100Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.filial = None
        self.mapa_documentos = {}
        self.tabela = "registro_c100"
        self.nome = "C100"

    def set_context(self, periodo, filial):
        self.periodo = periodo
        self.filial = filial

    def sanitizarPartes(self, partes: list[str]) -> list[str]:
        return (partes + [None] * (29 - len(partes)))[:29]

    def processar(self, partes: list[str]):
        partes = self.sanitizarPartes(partes)

        dados = {
            "reg": partes[0],
            "ind_oper": partes[1],
            "ind_emit": partes[2],
            "cod_part": partes[3],
            "cod_mod": partes[4],
            "cod_sit": partes[5],
            "ser": partes[6],
            "num_doc": partes[7],
            "chv_nfe": partes[8],
            "dt_doc": parseDate(partes[9]),
            "dt_e_s": parseDate(partes[10]),
            "vl_doc": parseDecimal(partes[11]),
            "ind_pgto": partes[12],
            "vl_desc": parseDecimal(partes[13]),
            "vl_abat_nt": parseDecimal(partes[14]),
            "vl_merc": parseDecimal(partes[15]),
            "ind_frt": partes[16],
            "vl_frt": parseDecimal(partes[17]),
            "vl_seg": parseDecimal(partes[18]),
            "vl_out_da": parseDecimal(partes[19]),
            "vl_bc_icms": parseDecimal(partes[20]),
            "vl_icms": parseDecimal(partes[21]),
            "vl_bc_icms_st": parseDecimal(partes[22]),
            "vl_icms_st": parseDecimal(partes[23]),
            "vl_ipi": parseDecimal(partes[24]),
            "vl_pis": parseDecimal(partes[25]),
            "vl_cofins": parseDecimal(partes[26]),
            "vl_pis_st": parseDecimal(partes[27]),
            "vl_cofins_st": parseDecimal(partes[28]),
            "periodo": self.periodo,
            "filial": self.filial,
            "empresa_id": self.empresa_id,
            "ativo": True
        }

        num_doc = str(partes[7] or "").zfill(9)

        self.mapa_documentos[num_doc] = {
            "ind_oper": partes[1],
            "cod_part": partes[3],
            "chv_nfe": partes[8],
            "dt_doc": parseDate(partes[9]),
        }

        ok, erros =  ValidadorService.validarRegistroC100(dados)
        if ok:
            self.lote.append(dados)
        else:
            return

        return {
            "num_doc": num_doc,
            "dt_doc": dados["dt_doc"],
            "chv_nfe": partes[8],
        }

    def getDocumentos(self) -> dict:
        return self.mapa_documentos

    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
