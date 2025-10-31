import pandas as pd

class Registro0200Repository:
    def __init__(self, session):
        self.session = session
        self.tabela = "registro_0200"

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "reg", "cod_item", "descr_item", "cod_barra",
            "cod_ant_item", "unid_inv", "tipo_item", "cod_ncm", "ex_ipi",
            "cod_gen", "cod_list", "aliq_icms", "cest",
            "periodo", "ativo"
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
            print(f"[DEBUG 0200] {len(df)} registros inseridos")
        except Exception as e:
            self.session.rollback()
            print(f"[ERRO] Falha ao salvar registros 0200: {e}")
            raise
