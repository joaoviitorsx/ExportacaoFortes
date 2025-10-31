from typing import List
from ....src.services.etl.leitorService import LeitorService
from ....src.services.etl.persistenciaService import PersistenciaService
from ....src.services.etl.softDeleteService import SoftDeleteService
from ....src.services.fornecedor.fornecedorService import FornecedorService
from ....src.repositories.fornecedoresRepo.fornecedorRepository import FornecedorRepository


from sqlalchemy.orm import sessionmaker

class PipelineService:
    def __init__(self, session, empresa_id: int, arquivos: List[str]):
        self.session = session
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        self.leitor = LeitorService(session, empresa_id)
        self.persistencia = PersistenciaService(session)

    def executar(self):
        try:
            print("Iniciando soft delete...")
            SoftDeleteService.softDelete(self.session, self.empresa_id)
        except Exception:
            self.session.rollback()

        for arquivo in self.arquivos:
            try:
                dados = self.leitor.lerArquivo(arquivo)
                self.persistencia.salvar(dados)
            except Exception as e:
                print(f"[ERRO] Falha ao processar {arquivo}: {e}")
                self.session.rollback()
                continue

        self.session.commit()
        self.session.close()

        SessionLocal = sessionmaker(bind=self.session.bind)
        nova_sessao = SessionLocal()

        try:
            fornecedor_repo = FornecedorRepository(nova_sessao)
            fornecedor_service = FornecedorService(fornecedor_repo)
            fornecedor_service.processar(self.empresa_id)
        finally:
            nova_sessao.close()
