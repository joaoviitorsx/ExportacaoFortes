from ....services.fs.CAB.builderCAB import builderCAB
from ....repositories.camposRepo.cab_repository import CabRepository

class ExportarCAB:
    def __init__(self, session):

        self.session = session
        self.repo = CabRepository(session)

    def gerar(self, empresa_id: int) -> str:
        empresa = self.repo.get_empresa(empresa_id)
        registro_0000 = self.repo.get_registro0000(empresa_id)

        if not empresa or not registro_0000:
            raise ValueError("Dados insuficientes para gerar CAB")

        return builderCAB(empresa, registro_0000)
