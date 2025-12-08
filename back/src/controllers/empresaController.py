from ..config.db.conexaoFS import getSessionFS
from ..repositories.empresaRepo.empresaRepository import EmpresaRepository
from ..services.cnpjRegister.cnpjService import CnpjService

class EmpresaController:
    def __init__(self):
        self.session = getSessionFS()
        self.repo = EmpresaRepository(self.session)

    def listarEmpresas(self):
        return self.repo.get_all()

    def cadastrarEmpresas(self, razao_social: str, cnpj: str, uf: str, simples: bool):
        return self.repo.insert(razao_social, cnpj, uf, simples)
    
    def buscarCnpj(self, cnpj: str):
        return CnpjService.consultarCnpj(cnpj)