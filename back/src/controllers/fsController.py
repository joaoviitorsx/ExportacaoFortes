import os
from ..config.db.conexaoFS import getSessionFS
from ..config.db.conexaoICMS import getSessionICMS
from ..services.exportar.gerarArquivo import GerarArquivo
from ..services.etl.pipelineService import PipelineService
from ..services.sync.transferDataService import TransferDataService


class FsController:
    def __init__(self, empresa_id: int, arquivos: list[str], output_path: str):
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        self.output_path = output_path

    def processar(self) -> list:
        etapas = []
        session_icms = getSessionICMS()
        session_fs = getSessionFS()

        try:
            etapas.append({"percent": 30, "mensagem": "Sincronizando produtos..."})
            transfer = TransferDataService(session_icms, session_fs)
            transfer.sincronizarEmpresa(self.empresa_id)

            etapas.append({"percent": 60, "mensagem": "Processando arquivos SPED..."})
            caminhos = [os.path.abspath(f) for f in self.arquivos]
            pipeline = PipelineService(session_fs, self.empresa_id, caminhos)
            pipeline.executar()

            etapas.append({"percent": 100, "mensagem": "Processamento concluído"})
            print(" 👌 Processamento concluído com sucesso")
            return etapas
            
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            raise
        finally:
            if session_icms:
                session_icms.close()
            if session_fs:
                session_fs.close()

    def arquivoFs(self) -> str:
        gerador = GerarArquivo(self.empresa_id, self.output_path)
        try:
            file_path = gerador.gerar()
            return file_path
        except Exception as e:
            print(f"❌ Erro ao gerar arquivo .fs: {e}")
            raise
        finally:
            del gerador