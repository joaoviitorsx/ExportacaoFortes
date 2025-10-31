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

    def set_context(self, periodo: str, filial: str):
        """Define o contexto (período e filial) para processamento"""
        self.periodo = periodo
        self.filial = filial

    def processar(self, partes: list[str]):
        """
        Processa registro C100 (Documento Fiscal)
        
        Layout C100 (Guia Prático EFD-ICMS/IPI):
        01 REG
        02 IND_OPER
        03 IND_EMIT
        04 COD_PART
        05 COD_MOD
        06 COD_SIT
        07 SER
        08 NUM_DOC
        09 CHV_NFE
        10 DT_DOC
        11 DT_E_S
        12 VL_DOC
        13 IND_PGTO
        14 VL_DESC
        15 VL_ABAT_NT
        16 VL_MERC
        17 IND_FRT
        18 VL_FRT
        19 VL_SEG
        20 VL_OUT_DA
        21 VL_BC_ICMS
        22 VL_ICMS
        23 VL_BC_ICMS_ST
        24 VL_ICMS_ST
        25 VL_IPI
        26 VL_PIS
        27 VL_COFINS
        28 VL_PIS_ST
        29 VL_COFINS_ST
        """
        if not self.periodo or not self.filial:
            print(f"[ERRO C100] Contexto não definido: periodo={self.periodo}, filial={self.filial}")
            return None

        # Expandir lista para 29 campos
        partes = (partes + [None] * 29)[:29]

        try:
            # Validação de campos obrigatórios
            num_doc = partes[7]
            if not num_doc:
                return None

            dados = {
                "reg": partes[0],
                "ind_oper": partes[1],
                "ind_emit": partes[2],
                "cod_part": partes[3],
                "cod_mod": partes[4],
                "cod_sit": partes[5],
                "ser": partes[6],
                "num_doc": num_doc,
                "chv_nfe": partes[8] or "",
                "dt_doc": self._to_date(partes[9]),
                "dt_e_s": self._to_date(partes[10]),
                "vl_doc": self._to_decimal(partes[11]),
                "ind_pgto": partes[12],
                "vl_desc": self._to_decimal(partes[13]),
                "vl_abat_nt": self._to_decimal(partes[14]),
                "vl_merc": self._to_decimal(partes[15]),
                "ind_frt": partes[16],
                "vl_frt": self._to_decimal(partes[17]),
                "vl_seg": self._to_decimal(partes[18]),
                "vl_out_da": self._to_decimal(partes[19]),
                "vl_bc_icms": self._to_decimal(partes[20]),
                "vl_icms": self._to_decimal(partes[21]),
                "vl_bc_icms_st": self._to_decimal(partes[22]),
                "vl_icms_st": self._to_decimal(partes[23]),
                "vl_ipi": self._to_decimal(partes[24]),
                "vl_pis": self._to_decimal(partes[25]),
                "vl_cofins": self._to_decimal(partes[26]),
                "vl_pis_st": self._to_decimal(partes[27]),
                "vl_cofins_st": self._to_decimal(partes[28]),
                # *** ADICIONAR CONTEXTO ***
                "periodo": self.periodo,
                "filial": self.filial,
                "ativo": True
            }

            return dados

        except Exception as e:
            print(f"[ERRO C100] Falha ao processar: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _to_decimal(self, valor):
        """Converte string para decimal, retorna 0 se inválido"""
        if not valor or valor in ("", "None"):
            return 0
        try:
            return float(valor.replace(",", "."))
        except:
            return 0

    def _to_date(self, valor):
        """Converte string DDMMYYYY para formato YYYY-MM-DD"""
        if not valor or len(valor) != 8:
            return None
        try:
            dia = valor[:2]
            mes = valor[2:4]
            ano = valor[4:]
            return f"{ano}-{mes}-{dia}"
        except:
            return None