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
        """
        Sincroniza produtos com INSERT + UPDATE automático.
        - Produtos novos: INSERT
        - Produtos existentes: UPDATE com novos valores
        """
        if df.empty:
            print("[INFO] Nenhum dado encontrado para inserção.")
            return

        df["empresa_id"] = empresa_id

        # Query com INSERT ON DUPLICATE KEY UPDATE
        upsert_query = text("""
            INSERT INTO produtos (codigo, produto, ncm, aliquota, categoriaFiscal, empresa_id)
            VALUES (:codigo, :produto, :ncm, :aliquota, :categoriaFiscal, :empresa_id)
            ON DUPLICATE KEY UPDATE
                produto = VALUES(produto),
                ncm = VALUES(ncm),
                aliquota = VALUES(aliquota),
                categoriaFiscal = VALUES(categoriaFiscal),
                empresa_id = VALUES(empresa_id)
        """)

        dados = df.to_dict(orient="records")

        # Executar em lote
        self.session.execute(upsert_query, dados)
        self.session.commit()

        print(f"[SUCESSO] {len(dados)} produtos sincronizados (novos inseridos + existentes atualizados).")