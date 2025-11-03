from typing import List, Callable, Optional
from ....src.services.etl.leitorService import LeitorService
from ....src.services.etl.persistenciaService import PersistenciaService
from ....src.services.etl.softDeleteService import SoftDeleteService
from ....src.services.fornecedor.fornecedorService import FornecedorService
from ....src.repositories.fornecedoresRepo.fornecedorRepository import FornecedorRepository

from sqlalchemy.orm import sessionmaker


class PipelineService:
    def __init__(self, session, empresa_id: int, arquivos: List[str],progress_callback: Optional[Callable[[int, str], None]] = None):
        self.session = session
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        self.leitor = LeitorService(session, empresa_id)
        self.persistencia = PersistenciaService(session)
        self.progress_callback = progress_callback

    def notificarProgresso(self, percent: int, mensagem: str):
        if self.progress_callback:
            self.progress_callback(percent, mensagem)

    def executar(self):
        try:
            self.notificarProgresso(40, "Limpando dados anteriores (soft delete)...")
            print("Iniciando soft delete...")
            SoftDeleteService.softDelete(self.session, self.empresa_id)
            self.notificarProgresso(45, "Soft delete concluído")
        except Exception as e:
            print(f"[ERRO] Falha no soft delete: {e}")
            self.session.rollback()

        total_arquivos = len(self.arquivos)
        percent_por_arquivo = 40 / total_arquivos if total_arquivos > 0 else 0
        
        for idx, arquivo in enumerate(self.arquivos, 1):
            try:
                percent_base = 45 + int((idx - 1) * percent_por_arquivo)
                nome_arquivo = arquivo.split('\\')[-1] if '\\' in arquivo else arquivo.split('/')[-1]
                
                # Leitura do arquivo
                self.notificarProgresso(
                    percent_base, 
                    f"Lendo arquivo {idx}/{total_arquivos}: {nome_arquivo}..."
                )
                
                dados = self.leitor.lerArquivo(arquivo)
                
                # Salvando dados
                self.notificarProgresso(
                    percent_base + int(percent_por_arquivo * 0.3),
                    f"Processando registros do arquivo {idx}/{total_arquivos}..."
                )
                
                # Salvar com feedback detalhado
                self.salvarProgresso(dados, percent_base, percent_por_arquivo, idx, total_arquivos)
                
                self.notificarProgresso(
                    percent_base + int(percent_por_arquivo),
                    f"Arquivo {idx}/{total_arquivos} processado com sucesso"
                )
                
            except Exception as e:
                print(f"[ERRO] Falha ao processar {arquivo}: {e}")
                self.notificarProgresso(
                    percent_base,
                    f"Erro ao processar arquivo {idx}/{total_arquivos}: {str(e)[:50]}..."
                )
                self.session.rollback()
                continue

        self.notificarProgresso(85, "Salvando todas as alterações no banco...")
        self.session.commit()
        self.session.close()
        self.notificarProgresso(88, "Dados salvos com sucesso")

        self.notificarProgresso(88, "Processando fornecedores...")
        SessionLocal = sessionmaker(bind=self.session.bind)
        nova_sessao = SessionLocal()

        try:
            fornecedor_repo = FornecedorRepository(nova_sessao)
            fornecedor_service = FornecedorService(fornecedor_repo)
            
            self.notificarProgresso(90, "Sincronizando dados de fornecedores...")
            fornecedor_service.processar(self.empresa_id)
            
            self.notificarProgresso(95, "Fornecedores processados com sucesso")
        except Exception as e:
            print(f"[ERRO] Falha ao processar fornecedores: {e}")
            self.notificarProgresso(95, "Erro ao processar fornecedores")
        finally:
            nova_sessao.close()

    def salvarProgresso(self, dados: dict, percent_base: int, percent_range: float, idx: int, total: int):
        if not dados:
            return
        
        tipos_registro = ['0000', '0150', '0190', '0200', '0210', 'C100', 'C170', 'C190', 'D100', 'E110']
        total_tipos = len([t for t in tipos_registro if t in dados])
        
        if total_tipos == 0:
            self.persistencia.salvar(dados)
            return
        
        percent_por_tipo = (percent_range * 0.6) / total_tipos if total_tipos > 0 else 0
        tipo_atual = 0
        
        for tipo in tipos_registro:
            if tipo in dados and dados[tipo]:
                tipo_atual += 1
                percent = percent_base + int(percent_por_tipo * tipo_atual) + int(percent_range * 0.3)
                
                qtd_registros = len(dados[tipo]) if isinstance(dados[tipo], list) else 1
                self.notificarProgresso(
                    percent,
                    f"Salvando registros {tipo} do arquivo {idx}/{total} ({qtd_registros} registro(s))..."
                )
                
                self.persistencia.salvar({tipo: dados[tipo]})