from back.src.controllers.fsController import FsController
from typing import Callable, Optional
from sqlalchemy.exc import OperationalError

class FsRoute:
    
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
            controller = FsController(
                empresa_id=empresa_id,
                arquivos=arquivos,
                output_path=output_path,
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