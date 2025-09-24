import pandas as pd

class RegistroC170Repository:
    def __init__(self, session):
        self.session = session
        self.tabela = "registro_c170"

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "periodo", "reg", "num_item", "cod_item", "descr_compl",
            "qtd", "unid", "vl_item", "vl_desc", "ind_mov", "cst_icms", "cfop",
            "cod_nat", "vl_bc_icms", "aliq_icms", "vl_icms", "vl_bc_icms_st",
            "aliq_st", "vl_icms_st", "ind_apur", "cst_ipi", "cod_enq", "vl_bc_ipi",
            "aliq_ipi", "vl_ipi", "cst_pis", "vl_bc_pis", "aliq_pis", "quant_bc_pis",
            "aliq_pis_reais", "vl_pis", "cst_cofins", "vl_bc_cofins", "aliq_cofins",
            "quant_bc_cofins", "aliq_cofins_reais", "vl_cofins", "cod_cta", "vl_abat_nt",
            "c100_id", "filial", "ind_oper", "cod_part", "num_doc", "chv_nfe",
            "ncm", "mercado", "aliquota", "resultado", "ativo"
        ]
        df = df.reindex(columns=colunas)

        try:
            df.to_sql(
                self.tabela,
                self.session.bind,
                if_exists="append",
                index=False,
                method="multi",
            )
        except Exception as e:
            self.session.rollback()
            print(f"[ERRO] Falha ao salvar registros C170: {e}")
            raise
