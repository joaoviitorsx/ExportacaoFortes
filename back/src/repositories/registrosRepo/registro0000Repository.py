import pandas as pd

class Registro0000Repository:
    def __init__(self, session):
        self.session = session
        self.tabela = "registro_0000"

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "reg", "cod_ver", "cod_fin", "dt_ini", "dt_fin",
            "nome", "cnpj", "cpf", "uf", "ie", "cod_num", "im", "suframa",
            "ind_perfil", "ind_ativ", "filial", "periodo", "ativo"
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
            print(f"[ERRO] Falha ao salvar registros 0000: {e}")
            raise
