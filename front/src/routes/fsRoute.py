from back.src.controllers.fsController import FsController
from typing import Callable, Optional
import os
from sqlalchemy.exc import OperationalError

class FsRoute:
    @staticmethod
    def _normalizarOutputPath(output_path: str) -> str:
        if not output_path:
            raise ValueError("Caminho de saída não informado.")

        path = os.path.abspath(os.path.expanduser(output_path.strip()))

        if os.path.isdir(path):
            path = os.path.join(path, "Exportacao_Fortes.fs")

        if not path.lower().endswith(".fs"):
            path = f"{path}.fs"

        dir_name = os.path.dirname(path) or "."
        if not os.path.isdir(dir_name):
            raise ValueError("Diretório de saída inválido ou inexistente.")

        return path
    
    @staticmethod
    def processarFs(empresa_id: int,  arquivos: list[str], output_path: str, progress_callback: Optional[Callable[[int, str], None]] = None):
        try:
            controller = FsController(
                empresa_id=empresa_id,
                arquivos=arquivos,
                output_path=output_path,
                progress_callback=progress_callback
            )
            etapas = controller.processar()
            
            return {
                "status": "ok",
                "mensagem": "Processamento concluído com sucesso!",
                "etapas": etapas
            }
        except OperationalError as e:
            # Erro de conexão com o banco (timeout, sem VPN, etc)
            error_str = str(e)
            print(f"[ERRO] Falha ao processar FS: {e}")
            
            if "2003" in error_str or "timed out" in error_str or "Can't connect" in error_str:
                error_msg = "Conexão com a VPN ou Rede não estabelecida. Conecte-se à VPN para retornar."
                if progress_callback:
                    progress_callback(0, error_msg)
                return {
                    "status": "erro",
                    "mensagem": error_msg,
                    "etapas": [],
                    "erro": "vpn"
                }
            
            error_msg = "Erro de conexão com o banco de dados."
            if progress_callback:
                progress_callback(0, error_msg)
            return {
                "status": "erro",
                "mensagem": error_msg,
                "etapas": []
            }
        except Exception as e:
            error_msg = f"Erro ao processar: {str(e)}"
        
            if progress_callback:
                progress_callback(0, error_msg)
            
            return {
                "status": "erro",
                "mensagem": error_msg,
                "etapas": []
            }
    
    @staticmethod
    def baixarFs(empresa_id: int, arquivos: list[str], output_path: str, progress_callback: Optional[Callable[[int, str], None]] = None):
        try:
            output_path_normalizado = FsRoute._normalizarOutputPath(output_path)
            print(f"[DEBUG] FsRoute.baixarFs output_path normalizado: {output_path_normalizado}")

            controller = FsController(
                empresa_id=empresa_id,
                arquivos=arquivos,
                output_path=output_path_normalizado,
                progress_callback=progress_callback
            )
            
            if progress_callback:
                progress_callback(0, "Iniciando geração do arquivo .fs...")
            
            file_path = controller.arquivoFs()
            
            if progress_callback:
                progress_callback(100, "Arquivo .fs gerado com sucesso!")
            
            return {
                "status": "ok",
                "mensagem": f"Arquivo gerado em {file_path}",
                "file_path": file_path
            }
        except OperationalError as e:
            # Erro de conexão com o banco (timeout, sem VPN, etc)
            error_str = str(e)
            print(f"[ERRO] Falha ao gerar arquivo FS: {e}")
            
            if "2003" in error_str or "timed out" in error_str or "Can't connect" in error_str:
                error_msg = "Conexão com a VPN ou Rede não estabelecida. Conecte-se à VPN para retornar."
                if progress_callback:
                    progress_callback(0, error_msg)
                return {
                    "status": "erro",
                    "mensagem": error_msg,
                    "file_path": None,
                    "erro": "vpn"
                }
            
            error_msg = "Erro de conexão com o banco de dados."
            if progress_callback:
                progress_callback(0, error_msg)
            return {
                "status": "erro",
                "mensagem": error_msg,
                "file_path": None
            }
        except Exception as e:
            error_msg = f"Erro ao gerar arquivo: {str(e)}"
            
            if progress_callback:
                progress_callback(0, error_msg)
            
            return {
                "status": "erro",
                "mensagem": error_msg,
                "file_path": None
            }
