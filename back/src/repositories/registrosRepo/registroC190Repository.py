import pandas as pd

class RegistroC190Repository:
    def __init__(self, session):
        self.session = session
        self.tabela = "registro_c190"

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "periodo", "c100_id", "reg",
            "cst_icms", "cfop", "aliq_icms", "vl_opr",
            "vl_bc_icms", "vl_icms", "vl_bc_icms_st", "vl_icms_st",
            "vl_red_bc", "vl_ipi", "cod_obs", "ativo"
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
            print(f"[ERRO] Falha ao salvar registros C190: {e}")
            raise