from back.src.controllers.empresaController import EmpresaController

class EmpresaRoute:
    @staticmethod
    def listar_empresas():
        try:
            controller = EmpresaController()
            return controller.listar_empresas()
        except Exception as e:
            print(f"[ERRO] Falha ao listar empresas: {e}")
            return []

    @staticmethod
    def cadastrar_empresa(razao_social: str, cnpj: str):
        try:
            controller = EmpresaController()
            return controller.cadastrar_empresa(razao_social, cnpj)
        except Exception as e:
            print(f"[ERRO] Falha ao cadastrar empresa: {e}")
            return None