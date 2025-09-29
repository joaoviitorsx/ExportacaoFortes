from ..config.db.conexaoFS import getSessionFS
from ..repositories.empresaRepo.empresaRepository import EmpresaRepository

class EmpresaController:
    def __init__(self):
        self.session = getSessionFS()
        self.repo = EmpresaRepository(self.session)

    def listar_empresas(self):
        return self.repo.get_all()

    def cadastrar_empresa(self, razao_social: str, cnpj: str):
        return self.repo.insert(razao_social, cnpj)