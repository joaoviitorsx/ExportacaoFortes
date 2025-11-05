from sqlalchemy import text
from .builderPRO import builderPRO
from ....repositories.camposRepo.pro_repository import ProRepository

class ExportarPRO:
    def __init__(self, session):
        self.session = session
        self.repo = ProRepository(session)

    def gerar(self, empresa_id: int) -> list[str]:
        produtos = self.repo.get_produtos(empresa_id)

        if not produtos:
            return []

        linhas_pro = [builderPRO(p) for p in produtos]
        
        return linhas_pro