import pandas as pd

class Registro0220Repository:
    def __init__(self, session):
        self.session = session
        self.tabela = "registro_0220"

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "periodo", "reg", "cod_item", "unid_conv", "fat_conv", "cod_barra","ativo"
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
            print(f"[DEBUG 0220] {len(df)} registros inseridos")
        except Exception as e:
            self.session.rollback()
            print(f"[ERRO] Falha ao salvar registros 0220: {e}")
            raise