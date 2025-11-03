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

    def inserirDados(self, df: pd.DataFrame, empresa_id: int):
        if df.empty:
            print("[INFO] Nenhum dado encontrado para inserção.")
            return

        df["empresa_id"] = empresa_id

        insert_query = text("""
            INSERT IGNORE INTO produtos (codigo, produto, ncm, aliquota, categoriaFiscal, empresa_id)
            VALUES (:codigo, :produto, :ncm, :aliquota, :categoriaFiscal, :empresa_id)
        """)

        dados = df.to_dict(orient="records")

        self.session.execute(insert_query, dados)
        self.session.commit()

        print(f"[INFO] Inserção concluída ({len(dados)} registros processados, duplicados ignorados).")
