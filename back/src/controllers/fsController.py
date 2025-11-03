import os
from typing import Callable, Optional
from ..config.db.conexaoFS import getSessionFS
from ..config.db.conexaoICMS import getSessionICMS
from ..services.exportar.gerarArquivo import GerarArquivo
from ..services.etl.pipelineService import PipelineService
from ..services.sync.transferDataService import TransferDataService
from ..utils.validadores import validarSpedFiscal


class FsController:
    def __init__(self, empresa_id: int, arquivos: list[str], output_path: str,progress_callback: Optional[Callable[[int, str], None]] = None):
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        self.output_path = output_path
        self.progress_callback = progress_callback

    def notificarProgresso(self, percent: int, mensagem: str):
        if self.progress_callback:
            self.progress_callback(percent, mensagem)

    def processar(self) -> list:
        etapas = []
        session_icms = None
        session_fs = None

        try:
            self.notificarProgresso(0, "Validando arquivos SPED...")
            etapas.append({"percent": 0, "mensagem": "Validando arquivos SPED..."})
            
            total_arquivos = len(self.arquivos)
            arquivos_invalidos = []
            
            for idx, arquivo in enumerate(self.arquivos, 1):
                nome_arquivo = os.path.basename(arquivo)
                percent = int((idx / total_arquivos) * 3)
                
                self.notificarProgresso(
                    percent, 
                    f"Validando arquivo {idx}/{total_arquivos}: {nome_arquivo}..."
                )
                etapas.append({
                    "percent": percent, 
                    "mensagem": f"Validando arquivo {idx}/{total_arquivos}: {nome_arquivo}..."
                })
                
                try:
                    validarSpedFiscal(arquivo)
                except ValueError as e:
                    arquivos_invalidos.append({
                        "arquivo": nome_arquivo,
                        "erro": str(e)
                    })
                except FileNotFoundError as e:
                    arquivos_invalidos.append({
                        "arquivo": nome_arquivo,
                        "erro": f"Arquivo não encontrado: {str(e)}"
                    })
            
            # Se houver arquivos inválidos, retorna erro
            if arquivos_invalidos:
                erros_detalhados = "\n".join([
                    f"• {inv['arquivo']}: {inv['erro']}" 
                    for inv in arquivos_invalidos
                ])
                mensagem_erro = f"Validação falhou:\n{erros_detalhados}"
                self.notificarProgresso(0, mensagem_erro)
                raise ValueError(mensagem_erro)
            
            self.notificarProgresso(3, "Todos os arquivos validados com sucesso")
            etapas.append({"percent": 3, "mensagem": "Todos os arquivos validados com sucesso"})
            
            self.notificarProgresso(5, "Conectando ao banco de dados...")
            etapas.append({"percent": 5, "mensagem": "Conectando ao banco de dados..."})
            
            session_icms = getSessionICMS()
            session_fs = getSessionFS()
            
            self.notificarProgresso(10, "Iniciando sincronização de produtos...")
            etapas.append({"percent": 10, "mensagem": "Iniciando sincronização de produtos..."})
            
            transfer = TransferDataService(session_icms, session_fs)
            transfer.sincronizarEmpresa(self.empresa_id)
            
            self.notificarProgresso(25, "Produtos sincronizados com sucesso")
            etapas.append({"percent": 25, "mensagem": "Produtos sincronizados com sucesso"})

            caminhos = []
            
            for idx, arquivo in enumerate(self.arquivos, 1):
                nome_arquivo = os.path.basename(arquivo)
                percent = 25 + int((idx / total_arquivos) * 15)
                
                self.notificarProgresso(percent, f"Preparando arquivo {idx}/{total_arquivos}: {nome_arquivo}")
                etapas.append({"percent": percent, "mensagem": f"Preparando arquivo {idx}/{total_arquivos}: {nome_arquivo}"})
                
                caminhos.append(os.path.abspath(arquivo))

            self.notificarProgresso(40, "Iniciando processamento dos registros SPED...")
            etapas.append({"percent": 40, "mensagem": "Iniciando processamento dos registros SPED..."})
            
            pipeline = PipelineService(session_fs, self.empresa_id, caminhos, self.notificarProgresso)
            pipeline.executar()

            self.notificarProgresso(95, "Finalizando processamento...")
            etapas.append({"percent": 95, "mensagem": "Finalizando processamento..."})
            
            self.notificarProgresso(100, "Processamento concluído com sucesso!")
            etapas.append({"percent": 100, "mensagem": "Processamento concluído com sucesso!"})
            
            print(" 👌 Processamento concluído com sucesso")
            return etapas
            
        except ValueError as ve:
            mensagem_erro = str(ve)
            self.notificarProgresso(0, mensagem_erro)
            print(f"❌ Erro de validação: {mensagem_erro}")
            raise
        except Exception as e:
            mensagem_erro = f"Erro no processamento: {str(e)}"
            self.notificarProgresso(0, mensagem_erro)
            print(f"❌ {mensagem_erro}")
            raise
        finally:
            if session_icms:
                session_icms.close()
            if session_fs:
                session_fs.close()

    def arquivoFs(self) -> str:
        """Gera o arquivo .fs"""
        gerador = GerarArquivo(self.empresa_id, self.output_path)
        try:
            file_path = gerador.gerar()
            return file_path
        except Exception as e:
            mensagem_erro = f"Erro ao gerar arquivo .fs: {str(e)}"
            print(f"❌ {mensagem_erro}")
            raise
        finally:
            del gerador