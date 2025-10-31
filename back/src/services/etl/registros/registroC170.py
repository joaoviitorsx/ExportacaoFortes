class RegistroC170Service:
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
        Processa registro C170 (Itens do Documento Fiscal)
        
        Layout C170 (Guia Prático EFD-ICMS/IPI):
        01 REG
        02 NUM_ITEM
        03 COD_ITEM
        04 DESCR_COMPL
        05 QTD
        06 UNID
        07 VL_ITEM
        08 VL_DESC
        09 IND_MOV
        10 CST_ICMS
        11 CFOP
        12 COD_NAT
        13 VL_BC_ICMS
        14 ALIQ_ICMS
        15 VL_ICMS
        16 VL_BC_ICMS_ST
        17 ALIQ_ST
        18 VL_ICMS_ST
        19 IND_APUR
        20 CST_IPI
        21 COD_ENQ
        22 VL_BC_IPI
        23 ALIQ_IPI
        24 VL_IPI
        25 CST_PIS
        26 VL_BC_PIS
        27 ALIQ_PIS (%)
        28 QUANT_BC_PIS
        29 ALIQ_PIS (R$)
        30 VL_PIS
        31 CST_COFINS
        32 VL_BC_COFINS
        33 ALIQ_COFINS (%)
        34 QUANT_BC_COFINS
        35 ALIQ_COFINS (R$)
        36 VL_COFINS
        37 COD_CTA
        38 VL_ABAT_NT
        """
        if not self.periodo or not self.filial:
            print(f"[ERRO C170] Contexto não definido: periodo={self.periodo}, filial={self.filial}")
            return None

        # *** CORREÇÃO: Expandir lista para 38 campos ***
        partes = (partes + [None] * 38)[:38]

        try:
            # Campos obrigatórios
            cod_item = partes[2]
            if not cod_item:
                print(f"[WARN C170] cod_item vazio, registro ignorado")
                return None

            dados = {
                "reg": partes[0],
                "num_item": partes[1],
                "cod_item": cod_item,
                "descr_compl": partes[3] or "",
                "qtd": self._to_decimal(partes[4]),
                "unid": partes[5],
                "vl_item": self._to_decimal(partes[6]),
                "vl_desc": self._to_decimal(partes[7]),
                "ind_mov": partes[8],
                "cst_icms": partes[9],
                "cfop": partes[10],
                "cod_nat": partes[11],
                "vl_bc_icms": self._to_decimal(partes[12]),
                "aliq_icms": self._to_decimal(partes[13]),
                "vl_icms": self._to_decimal(partes[14]),
                "vl_bc_icms_st": self._to_decimal(partes[15]),
                "aliq_st": self._to_decimal(partes[16]),
                "vl_icms_st": self._to_decimal(partes[17]),
                "ind_apur": partes[18],
                "cst_ipi": partes[19],
                "cod_enq": partes[20],
                "vl_bc_ipi": self._to_decimal(partes[21]),
                "aliq_ipi": self._to_decimal(partes[22]),
                "vl_ipi": self._to_decimal(partes[23]),
                "cst_pis": partes[24],
                "vl_bc_pis": self._to_decimal(partes[25]),
                "aliq_pis": self._to_decimal(partes[26]),
                "quant_bc_pis": self._to_decimal(partes[27]),
                "aliq_pis_reais": self._to_decimal(partes[28]),
                "vl_pis": self._to_decimal(partes[29]),
                "cst_cofins": partes[30],
                "vl_bc_cofins": self._to_decimal(partes[31]),
                "aliq_cofins": self._to_decimal(partes[32]),
                "quant_bc_cofins": self._to_decimal(partes[33]),
                "aliq_cofins_reais": self._to_decimal(partes[34]),
                "vl_cofins": self._to_decimal(partes[35]),
                "cod_cta": partes[36],
                "vl_abat_nt": self._to_decimal(partes[37]),
                # Contexto
                "periodo": self.periodo,
                "filial": self.filial,
                "ativo": True
            }

            return dados

        except Exception as e:
            print(f"[ERRO C170] Falha ao processar: {e}")
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