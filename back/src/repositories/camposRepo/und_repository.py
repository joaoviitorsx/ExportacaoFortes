from typing import List, Dict
from sqlalchemy import text


class UndRepository:
    def __init__(self, session):
        self.session = session

    def listar_unidades(self, empresa_id: int) -> List[Dict]:
        query = text("""
            SELECT DISTINCT
                unid,
                descr
            FROM registro_0190
            WHERE empresa_id = :empresa_id
              AND ativo = TRUE
              AND unid IS NOT NULL
              AND unid <> ''
        """)

        rows = self.session.execute(
            query, {"empresa_id": empresa_id}
        ).mappings().all()

        return [dict(r) for r in rows]
