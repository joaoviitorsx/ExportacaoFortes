from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session
        self._empresa_table = None

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

    def _resolver_tabela_empresas(self) -> str:
        if self._empresa_table:
            return self._empresa_table

        # Compatibilidade:
        # - Schema antigo: empresas
        # - Schema novo (Apurador): company
        for table_name in ("empresas", "company"):
            if self._table_exists(table_name):
                self._empresa_table = table_name
                return table_name

        raise RuntimeError("Nenhuma tabela de empresas encontrada (esperado: empresas ou company).")

    @staticmethod
    def _normalizar_cnpj(cnpj: str) -> str:
        return "".join(ch for ch in str(cnpj or "") if ch.isdigit())

    def getID(self, empresa_id: int):
        tabela = self._resolver_tabela_empresas()
        if tabela == "empresas":
            query = text(
                """
                SELECT
                    id,
                    cnpj,
                    cnpj_raiz,
                    razao_social,
                    is_matriz,
                    matriz_id
                FROM empresas
                WHERE id = :id
                """
            )
        else:
            query = text(
                """
                SELECT
                    id,
                    cnpj,
                    NULL AS cnpj_raiz,
                    razao_social,
                    1 AS is_matriz,
                    id AS matriz_id
                FROM company
                WHERE id = :id
                """
            )
        return self.session.execute(query, {"id": empresa_id}).mappings().first()

    def getCnpj(self, cnpj: str):
        tabela = self._resolver_tabela_empresas()
        cnpj_limpo = self._normalizar_cnpj(cnpj)
        query = text(
            f"""
            SELECT id, cnpj, razao_social
            FROM {tabela}
            WHERE cnpj = :cnpj
               OR REPLACE(REPLACE(REPLACE(cnpj, '.', ''), '/', ''), '-', '') = :cnpj_limpo
            LIMIT 1
            """
        )
        return self.session.execute(query, {"cnpj": cnpj, "cnpj_limpo": cnpj_limpo}).mappings().first()
