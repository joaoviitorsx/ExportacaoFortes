from sqlalchemy import text

class ProRepository:
    def __init__(self, session):
        self.session = session 

    def get_produtos(self, empresa_id: int):
        query = text("""
            SELECT 
                cod_item, descr_item, cod_barra, unid_inv,
                cod_ncm, cod_gen, cest
            FROM registro_0200
            WHERE empresa_id = :empresa_id
                AND ativo = 1
        """)
        return self.session.execute(query, {"empresa_id": empresa_id}).mappings().all()