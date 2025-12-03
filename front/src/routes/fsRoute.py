from back.src.controllers.fsController import FsController
from typing import Callable, Optional

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
        except Exception as e:
            error_msg = f"Erro ao gerar arquivo: {str(e)}"
            
            if progress_callback:
                progress_callback(0, error_msg)
            
            return {
                "status": "erro",
                "mensagem": error_msg,
                "file_path": None
            }