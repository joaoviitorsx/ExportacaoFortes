from back.src.controllers.empresaController import EmpresaController
from back.src.utils.validadores import removedorCaracteres

class EmpresaRoute:
    @staticmethod
    def listarEmpresas():
        try:
            controller = EmpresaController()
            return controller.listarEmpresas()
        except Exception as e:
            print(f"[ERRO] Falha ao listar empresas: {e}")
            return []

    @staticmethod
    def cadastrarEmpresa(dados: dict):
        try:
            controller = EmpresaController()
            cnpjLimpo = removedorCaracteres(dados["cnpj"])
            return controller.cadastrarEmpresas(
                dados["razao_social"],
                cnpjLimpo,
                dados["uf"],
                dados["simples"],
                dados.get("aliq_espec", 0)
            )
        except Exception as e:
            print(f"[ERRO] Falha ao cadastrar empresa: {e}")
            return None

    @staticmethod
    def buscarCnpj(cnpj: str):
        try:
            controller = EmpresaController()
            return controller.buscarCnpj(cnpj)
        except Exception as e:
            print(f"[ERRO] Falha ao buscar CNPJ: {e}")
            return None