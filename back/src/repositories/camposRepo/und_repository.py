from typing import List, Dict
from sqlalchemy import text

class UndRepository:
    def __init__(self, session):
        self.session = session

    def get_unidades(self, empresa_id: int) -> List[Dict[str, str]]:
        query = text("""
            SELECT DISTINCT unid_inv
            FROM registro_0200
            WHERE empresa_id = :empresa_id
              AND unid_inv IS NOT NULL
              AND unid_inv != ''
              AND ativo = 1
        """)
        return self.session.execute(query, {"empresa_id": empresa_id}).mappings().all()
