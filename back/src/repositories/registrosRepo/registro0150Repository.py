import pandas as pd

class Registro0150Repository:
    def __init__(self, session):
        self.session = session
        self.tabela = "registro_0150"

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "reg", "cod_part", "nome", "cod_pais", "cnpj",
            "cpf", "ie", "cod_mun", "suframa", "ende", "num", "compl",
            "bairro", "uf", "tipo_pessoa", "periodo", "ativo"
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
            print(f"[ERRO] Falha ao salvar registros 0150: {e}")
            raise
