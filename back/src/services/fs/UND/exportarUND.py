from sqlalchemy import text
from ....services.fs.UND.builderUND import builderUND

class ExportarUND:
    def __init__(self, session):
        self.session = session

    def gerar(self, empresa_id: int) -> list[str]:
        query = text("""
            SELECT DISTINCT unid_inv
            FROM registro_0200
            WHERE empresa_id = :empresa_id AND unid_inv IS NOT NULL AND unid_inv != ''
        """)
        
        resultado = self.session.execute(query, {"empresa_id": empresa_id}).mappings().all()

        if not resultado:
            return []

        unidades_unicas = {item['unid_inv'] for item in resultado}

        linhas_und = [builderUND(unidade_sigla) for unidade_sigla in sorted(list(unidades_unicas))]
        
        return linhas_und