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

    def processar(self) -> str:
        # 1. Rodar ETL e persistir registros
        session = getSessionFS()
        pipeline = PipelineService(session, self.empresa_id, self.arquivos)
        pipeline.executar()

        # 2. Sincronizar produtos entre ICMS e Exportação
        session_icms = getSessionICMS()
        session_export = getSessionFS()
        transfer = TransferDataService(session_icms, session_export)
        transfer.sincronizarEmpresa(self.empresa_id)

        # 3. Atualizar fornecedores
        repo = FornecedorRepository(session_export)
        fornecedor_service = FornecedorService(repo)
        fornecedor_service.processar(self.empresa_id)

        # 4. Gerar arquivo .fs
        gerador = GerarArquivo(self.empresa_id, self.output_path)
        file_path = gerador.gerar()

        print("Processo finalizado com sucesso!")
        return file_path
