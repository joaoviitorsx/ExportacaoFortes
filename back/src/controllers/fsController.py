import os
from ..config.db.conexaoFS import getSessionFS
from ..config.db.conexaoICMS import getSessionICMS
from ..services.exportar.gerarArquivo import GerarArquivo
from ..services.etl.pipelineService import PipelineService
from ..services.sync.transferDataService import TransferDataService
from ..services.fornecedor.fornecedorService import FornecedorService
from ..repositories.fornecedoresRepo.fornecedorRepository import FornecedorRepository

class FsController:
    def __init__(self, empresa_id: int, arquivos: list[str], output_path: str):
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        self.output_path = output_path

    def processar(self) -> list:
        etapas = []

        session_icms = getSessionICMS()
        session_export = getSessionFS()

        etapas.append({"percent": 12, "mensagem": "Atualizando fornecedores..."})
        repo = FornecedorRepository(session_export)
        fornecedor_service = FornecedorService(repo)
        fornecedor_service.processar(self.empresa_id)
        
        etapas.append({"percent": 42, "mensagem": "Sincronizando produtos..."})
        transfer = TransferDataService(session_icms, session_export)
        transfer.sincronizarEmpresa(self.empresa_id)

        etapas.append({"percent": 72, "mensagem": "Executando ETL..."})
        session = getSessionFS()
        caminhos = [os.path.abspath(f) for f in self.arquivos]
        pipeline = PipelineService(session, self.empresa_id, caminhos)
        pipeline.executar()

        etapas.append({"percent": 100, "mensagem": "Processamento concluído."})

        return etapas

    def arquivoFs(self) -> str:
        gerador = GerarArquivo(self.empresa_id, self.output_path)
        file_path = gerador.gerar()
        print("Arquivo .fs gerado com sucesso!")
        return file_path