import pandas as pd
from sqlalchemy import text

class ProdutoRepository:
    def __init__(self, session):
        self.session = session
        self._tabela_origem = None
        self._tabela_destino = None

    def _table_exists(self, table_name: str) -> bool:
        try:
            query = text(
                """
                SELECT COUNT(*) AS total
                FROM information_schema.tables
                WHERE table_schema = DATABASE()
                  AND table_name = :table_name
                """
            )
            total = self.session.execute(query, {"table_name": table_name}).scalar() or 0
            return int(total) > 0
        except Exception:
            # Fallback para ambientes com restrição de acesso ao information_schema.
            try:
                self.session.execute(text(f"SELECT 1 FROM {table_name} LIMIT 1"))
                return True
            except Exception:
                return False

    def _resolver_tabela_origem(self) -> str:
        if self._tabela_origem:
            return self._tabela_origem

        # Compatibilidade:
        # - Schema novo (Apurador): products
        # - Schema antigo: cadastro_tributacao
        for table_name in ("products", "cadastro_tributacao"):
            if self._table_exists(table_name):
                self._tabela_origem = table_name
                return table_name

        raise RuntimeError("Nenhuma tabela de produtos de origem encontrada (products/cadastro_tributacao).")

    def _resolver_tabela_destino(self) -> str:
        if self._tabela_destino:
            return self._tabela_destino

        # Destino padrão do ExportacaoFortes é "produtos".
        # Fallback para "products" apenas para manter compatibilidade.
        for table_name in ("produtos", "products"):
            if self._table_exists(table_name):
                self._tabela_destino = table_name
                return table_name

        raise RuntimeError("Nenhuma tabela de produtos de destino encontrada (produtos/products).")

    def getEmpresa(self, empresa_id: int):
        tabela = self._resolver_tabela_origem()
        if tabela == "products":
            query = text(
                """
                SELECT codigo, produto, ncm, aliquota, categoriaFiscal
                FROM products
                WHERE empresa_id = :empresa_id
                  AND is_active = 1
                """
            )
        else:
            query = text(
                """
                SELECT codigo, produto, ncm, aliquota, categoriaFiscal
                FROM cadastro_tributacao
                WHERE empresa_id = :empresa_id
                """
            )
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
        tabela_destino = self._resolver_tabela_destino()

        if tabela_destino == "products":
            upsert_query = text(
                """
                INSERT INTO products (codigo, produto, ncm, aliquota, categoriaFiscal, empresa_id, is_active, pending_run_id)
                VALUES (:codigo, :produto, :ncm, :aliquota, :categoriaFiscal, :empresa_id, 1, NULL)
                ON DUPLICATE KEY UPDATE
                    produto = VALUES(produto),
                    ncm = VALUES(ncm),
                    aliquota = VALUES(aliquota),
                    categoriaFiscal = VALUES(categoriaFiscal),
                    empresa_id = VALUES(empresa_id),
                    is_active = 1,
                    pending_run_id = NULL
                """
            )
        else:
            # Query com INSERT ON DUPLICATE KEY UPDATE
            upsert_query = text(
                """
                INSERT INTO produtos (codigo, produto, ncm, aliquota, categoriaFiscal, empresa_id)
                VALUES (:codigo, :produto, :ncm, :aliquota, :categoriaFiscal, :empresa_id)
                ON DUPLICATE KEY UPDATE
                    produto = VALUES(produto),
                    ncm = VALUES(ncm),
                    aliquota = VALUES(aliquota),
                    categoriaFiscal = VALUES(categoriaFiscal),
                    empresa_id = VALUES(empresa_id)
                """
            )

        dados = df.to_dict(orient="records")

        # Executar em lote
        self.session.execute(upsert_query, dados)
        self.session.commit()

        print(f"[SUCESSO] {len(dados)} produtos sincronizados (novos inseridos + existentes atualizados).")
