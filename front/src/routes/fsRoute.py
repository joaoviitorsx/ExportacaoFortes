from back.src.controllers.fsController import FsController

class FsRoute:
    
    def processarFs(empresa_id: int, arquivos: list[str], output_path: str) -> str:
        try:
            controller = FsController(empresa_id, arquivos, output_path)
            caminho = controller.processar()
            return {
                "status": "ok",
                "mensagem": "Arquivo gerado com sucesso",
                "caminho": caminho
            }
        except Exception as e:
            return {
                "status": "erro",
                "mensagem": str(e),
                "caminho": None
            }