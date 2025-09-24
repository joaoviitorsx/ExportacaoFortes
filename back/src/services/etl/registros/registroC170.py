import pandas as pd
from src.repositories.registrosFS.registroC170Repository import RegistroC170Repository
from src.utils.sanitizacao import (
    truncar, corrigirUnidade, corrigirIndMov, corrigirCstIcms,
    validarEstruturaC170, TAMANHOS_MAXIMOS, parseDecimal
)

class RegistroC170Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.repository = RegistroC170Repository(session)
        self.periodo = None
        self.filial = None
        self.mapa_documentos = {}
        self.lote = []
        self.tabela = "registro_c170"
        self.nome = "C170"

    def set_context(self, periodo, filial):
        self.periodo = periodo
        self.filial = filial

    def setDocumentos(self, mapa_documentos: dict):
        self.mapa_documentos = mapa_documentos

    def sanitizarPartes(self, partes: list[str]) -> list[str]:
        return (partes + [None] * (39 - len(partes)))[:39]

    def processar(self, partes: list[str], num_doc: str) -> None:
        partes = self.sanitizarPartes(partes)
        num_doc = str(num_doc).zfill(9)

        if not num_doc or len(partes) < 10:
            return None

        doc_info = self.mapa_documentos.get(num_doc)
        if not doc_info:
            return None

        try:
            num_item = str(int(partes[1])).zfill(3)[:3]
        except Exception:
            return None

        cod_item = partes[2]
        if cod_item is not None:
            cod_item = cod_item.lstrip("0") or "0"

        dados = {
            "periodo": self.periodo,
            "reg": partes[0],  # C170
            "num_item": num_item,
            "cod_item": truncar(cod_item, TAMANHOS_MAXIMOS['cod_item']),
            "descr_compl": truncar(partes[3], TAMANHOS_MAXIMOS['descr_compl']),
            "qtd": parseDecimal(partes[4]),
            "unid": truncar(corrigirUnidade(partes[5]), TAMANHOS_MAXIMOS['unid']),
            "vl_item": parseDecimal(partes[6]),
            "vl_desc": parseDecimal(partes[7]) if partes[7] not in (None, '', ' ') else 0.00,
            "ind_mov": corrigirIndMov(partes[8]),
            "cst_icms": corrigirCstIcms(partes[9]),
            "cfop": partes[10],
            "cod_nat": truncar(partes[11], TAMANHOS_MAXIMOS['cod_nat']),
            "vl_bc_icms": parseDecimal(partes[12]),
            "aliq_icms": parseDecimal(partes[13]),
            "vl_icms": parseDecimal(partes[14]),
            "vl_bc_icms_st": parseDecimal(partes[15]),
            "aliq_st": parseDecimal(partes[16]),
            "vl_icms_st": parseDecimal(partes[17]),
            "ind_apur": partes[18],
            "cst_ipi": partes[19],
            "cod_enq": partes[20],
            "vl_bc_ipi": parseDecimal(partes[21]),
            "aliq_ipi": parseDecimal(partes[22]),
            "vl_ipi": parseDecimal(partes[23]),
            "cst_pis": partes[24],
            "vl_bc_pis": parseDecimal(partes[25]),
            "aliq_pis": parseDecimal(partes[26]),
            "quant_bc_pis": parseDecimal(partes[27]),
            "aliq_pis_reais": parseDecimal(partes[28]),
            "vl_pis": parseDecimal(partes[29]),
            "cst_cofins": partes[30],
            "vl_bc_cofins": parseDecimal(partes[31]),
            "aliq_cofins": parseDecimal(partes[32]),
            "quant_bc_cofins": parseDecimal(partes[33]),
            "aliq_cofins_reais": parseDecimal(partes[34]),
            "vl_cofins": parseDecimal(partes[35]),
            "cod_cta": truncar(partes[36], TAMANHOS_MAXIMOS['cod_cta']),
            "vl_abat_nt": parseDecimal(partes[37]),
            "filial": self.filial,
            "ind_oper": doc_info.get("ind_oper"),
            "cod_part": doc_info.get("cod_part"),
            "num_doc": num_doc,
            "chv_nfe": doc_info.get("chv_nfe"),
            "empresa_id": self.empresa_id,
            "ativo": True,
            # extras / defaults
            "ncm": "",
            "mercado": "",
            "aliquota": "",
            "resultado": None,
        }

        if not validarEstruturaC170(list(dados.values())):
            return None

        self.lote.append(dados)

    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
