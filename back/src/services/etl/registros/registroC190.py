class RegistroC190Service:
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

    def processar(self, partes: list[str], num_doc=None):
        """
        Processa registro C190 (Totalizador ICMS)
        
        Layout C190 (Guia Prático EFD-ICMS/IPI):
        01 REG
        02 CST_ICMS
        03 CFOP
        04 ALIQ_ICMS
        05 VL_OPR
        06 VL_BC_ICMS
        07 VL_ICMS
        08 VL_BC_ICMS_ST
        09 VL_ICMS_ST
        10 VL_RED_BC
        11 VL_IPI
        12 COD_OBS
        """
        if not self.periodo or not self.filial:
            print(f"[ERRO C190] Contexto não definido: periodo={self.periodo}, filial={self.filial}")
            return None

        # *** CORREÇÃO: Expandir lista para 12 campos ***
        partes = (partes + [None] * 12)[:12]

        try:
            dados = {
                "reg": partes[0],
                "cst_icms": partes[1],
                "cfop": partes[2],
                "aliq_icms": self._to_decimal(partes[3]),
                "vl_opr": self._to_decimal(partes[4]),
                "vl_bc_icms": self._to_decimal(partes[5]),
                "vl_icms": self._to_decimal(partes[6]),
                "vl_bc_icms_st": self._to_decimal(partes[7]),
                "vl_icms_st": self._to_decimal(partes[8]),
                "vl_red_bc": self._to_decimal(partes[9]),
                "vl_ipi": self._to_decimal(partes[10]),
                "cod_obs": partes[11],
                # Contexto
                "periodo": self.periodo,
                "ativo": True
            }

            return dados

        except Exception as e:
            print(f"[ERRO C190] Falha ao processar: {e}")
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