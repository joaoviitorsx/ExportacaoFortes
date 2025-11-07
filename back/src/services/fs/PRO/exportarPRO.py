from sqlalchemy import text
from .builderPRO import builderPRO
from ..OUM.exportarOUM import ExportarOUM
from ....repositories.camposRepo.pro_repository import ProRepository

class ExportarPRO:
    def __init__(self, session):
        self.session = session
        self.repo = ProRepository(session)
        self.exportar_oum = ExportarOUM(session)

    def gerar(self, empresa_id: int) -> list[str]:
        produtos = self.repo.get_produtos(empresa_id)

        if not produtos:
            return []

        oum_map = self.exportar_oum.gerar(produtos)

        linhas_pro = []
        
        for produto in produtos:
            cod_item = produto.get("cod_item")
            
            linha_pro = builderPRO(produto)
            linhas_pro.append(linha_pro)
            
            if cod_item in oum_map:
                linhas_pro.extend(oum_map[cod_item])
        
        return linhas_pro