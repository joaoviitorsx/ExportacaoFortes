import pandas as pd
from sqlalchemy import text

class ProdutoRepository:
    def __init__(self, session):
        self.session = session

    def getEmpresa(self, empresa_id: int):
        query = text("""
            SELECT codigo, produto, ncm, aliquota, categoriaFiscal
            FROM cadastro_tributacao
            WHERE empresa_id = :empresa_id
        """)
        return pd.read_sql_query(query, self.session.bind, params={"empresa_id": empresa_id})

    def inserirDados(self, df: pd.DataFrame):
        df.to_sql(
            "produtos",
            self.session.bind,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000
        )
