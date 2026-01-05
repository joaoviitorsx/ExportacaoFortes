from typing import Dict, List
from sqlalchemy import text

class OumRepository:
    def __init__(self, session):
        self.session = session

    def get_oum(self, empresa_id: int) -> Dict[str, List[dict]]:
        query = text("""
            SELECT
                cod_item,
                unid_conv,
                fat_conv
            FROM registro_0220
            WHERE empresa_id = :empresa_id
              AND ativo = TRUE
              AND unid_conv IS NOT NULL
        """)

        rows = self.session.execute(
            query, {"empresa_id": empresa_id}
        ).mappings().all()

        mapa: Dict[str, List[dict]] = {}

        for r in rows:
            cod = r["cod_item"]
            mapa.setdefault(cod, []).append({
                "unid_conv": r["unid_conv"],
                "fat_conv": r["fat_conv"]
            })

        return mapa
