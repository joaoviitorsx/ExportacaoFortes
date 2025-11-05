from sqlalchemy import text

class CabRepository:
    def __init__(self, session):
        self.session = session

    def get_empresa(self, empresa_id: int):
        query = text("""
            SELECT razao_social, aliq_espec
            FROM empresas
            WHERE id = :id
        """)
        return self.session.execute(query, {"id": empresa_id}).mappings().first()

    def get_registro0000(self, empresa_id: int):
        query = text("""
            SELECT dt_ini, dt_fin, periodo
            FROM registro_0000
            WHERE empresa_id = :id AND ativo = 1
            LIMIT 1
        """)
        return self.session.execute(query, {"id": empresa_id}).mappings().first()
