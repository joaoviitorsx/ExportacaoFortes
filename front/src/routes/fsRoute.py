from back.src.controllers.fsController import FsController

class FsRoute:
    
    def processarFs(empresa_id: int, arquivos: list[str], output_path: str):
        try:
            controller = FsController(empresa_id, arquivos, output_path)
            etapas = controller.processar()
            return {
                "status": "ok",
                "mensagem": "Processamento concluído",
                "etapas": etapas
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e),
                "etapas": []
            }
        
    def baixarFs(empresa_id: int, arquivos: list[str], output_path: str):
        try:
            controller = FsController(empresa_id, arquivos, output_path)
            file_path = controller.arquivoFs()
            return {
                "status": "ok",
                "mensagem": f"Arquivo gerado em {file_path}",
                "file_path": file_path
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e),
                "file_path": None
            }