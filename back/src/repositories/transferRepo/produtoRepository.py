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
            return

        # Buscar códigos já cadastrados no destino
        codigos_existentes = {
            row[0] for row in self.session.execute(
                text("SELECT codigo FROM produtos WHERE empresa_id = :empresa_id"),
                {"empresa_id": empresa_id}
            ).all()
        }

        # Filtrar apenas os que ainda não existem
        novos = df[~df["codigo"].isin(codigos_existentes)].copy()
        novos["empresa_id"] = empresa_id

        if novos.empty:
            print("[INFO] Nenhum produto novo para inserir.")
            return

        novos.to_sql(
            "produtos",
            self.session.bind,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000,
        )
        print(f"[INFO] {len(novos)} produtos novos inseridos.")
