from sqlalchemy import text
from src.services.fs.PRO.builderPRO import builderPRO

class ExportarPRO:
    def __init__(self, session):
        self.session = session

    def gerar(self, empresa_id: int) -> list[str]:
        query = text("""
            SELECT 
                cod_item, descr_item, cod_barra, unid_inv,
                cod_ncm, cod_gen, cest
            FROM registro_0200
            WHERE empresa_id = :empresa_id
        """)
        
        produtos = self.session.execute(query, {"empresa_id": empresa_id}).mappings().all()

        if not produtos:
            return []

        linhas_pro = [builderPRO(p) for p in produtos]
        
        return linhas_pro