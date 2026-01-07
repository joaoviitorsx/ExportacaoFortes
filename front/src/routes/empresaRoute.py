from back.src.controllers.empresaController import EmpresaController
from back.src.utils.validadores import removedorCaracteres
from sqlalchemy.exc import OperationalError

class EmpresaRoute:
    @staticmethod
    def listarEmpresas():
        try:
            controller = EmpresaController()
            return controller.listarEmpresas()
        except OperationalError as e:
            # Erro de conexão com o banco (timeout, sem VPN, etc)
            error_str = str(e)
            print(f"[ERRO] Falha ao listar empresas: {e}")
            # Verificar se é erro de timeout/conexão
            if "2003" in error_str or "timed out" in error_str or "Can't connect" in error_str:
                return {"erro": "vpn", "mensagem": "Conexão com a VPN ou Rede não estabelecida. Conecte-se à VPN para retornar."}
            return {"erro": "geral", "mensagem": "Erro de conexão com o banco de dados."}
        except Exception as e:
            print(f"[ERRO] Falha ao listar empresas: {e}")
            return {"erro": "geral", "mensagem": f"Erro ao listar empresas: {str(e)}"}

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
            )
        except OperationalError as e:
            # Erro de conexão com o banco (timeout, sem VPN, etc)
            error_str = str(e)
            print(f"[ERRO] Falha ao cadastrar empresa: {e}")
            if "2003" in error_str or "timed out" in error_str or "Can't connect" in error_str:
                return {"erro": "vpn", "mensagem": "Conexão com a VPN ou Rede não estabelecida. Conecte-se à VPN para retornar."}
            return {"erro": "geral", "mensagem": "Erro de conexão com o banco de dados."}
        except Exception as e:
            print(f"[ERRO] Falha ao cadastrar empresa: {e}")
            return {"erro": "geral", "mensagem": f"Erro ao cadastrar empresa: {str(e)}"}

    @staticmethod
    def buscarCnpj(cnpj: str):
        try:
            controller = EmpresaController()
            return controller.buscarCnpj(cnpj)
        except OperationalError as e:
            # Erro de conexão com o banco (timeout, sem VPN, etc)
            error_str = str(e)
            print(f"[ERRO] Falha ao buscar CNPJ: {e}")
            if "2003" in error_str or "timed out" in error_str or "Can't connect" in error_str:
                return {"erro": "vpn", "mensagem": "Conexão com a VPN ou Rede não estabelecida. Conecte-se à VPN para retornar."}
            return {"erro": "geral", "mensagem": "Erro de conexão com o banco de dados."}
        except Exception as e:
            print(f"[ERRO] Falha ao buscar CNPJ: {e}")
            return {"erro": "geral", "mensagem": f"Erro ao buscar CNPJ: {str(e)}"}