import pandas as pd

class Registro0221Repository:
    def __init__(self, session):
        self.session = session
        self.tabela = "registro_0221"

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "periodo", "reg", "cod_item", "cod_item_atomico","ativo"
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
            print(f"[DEBUG 0221] {len(df)} registros inseridos")
        except Exception as e:
            self.session.rollback()
            print(f"[ERRO] Falha ao salvar registros 0221: {e}")
            raise