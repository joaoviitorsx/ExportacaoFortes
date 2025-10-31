import asyncio
import concurrent.futures
from ...utils.cnpj import processarCnpjs
from ...repositories.fornecedoresRepo.fornecedorRepository import FornecedorRepository

LOTE = 50

class FornecedorService:
    def __init__(self, repository: FornecedorRepository):
        self.repository = repository

    async def _processar_async(self, empresa_id: int):
        print("Buscando novos fornecedores...")
        df_novos = self.repository.novosFornecedores(empresa_id)
        
        if not df_novos.empty:
            inseridos = self.repository.inserirFornecedores(empresa_id, df_novos)
            print(f"{inseridos} fornecedores inseridos")
        else:
            print("Nenhum fornecedor novo")

        print("Verificando CNPJs pendentes...")
        cnpjs = self.repository.cnpjsPendentes(empresa_id)
        
        if not cnpjs:
            print("Nenhum CNPJ pendente")
            return

        print(f"Consultando {len(cnpjs)} CNPJs...")
        resultados = await processarCnpjs(cnpjs)

        print("Atualizando fornecedores...")
        total_atualizado = 0
        for i in range(0, len(cnpjs), LOTE):
            batch = cnpjs[i:i + LOTE]
            atualizado = self.repository.atualizarFornecedores(empresa_id, resultados, batch)
            total_atualizado += atualizado
        
        print(f"{total_atualizado} fornecedores atualizados")

    def processar(self, empresa_id: int):
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    asyncio.run, 
                    self._processar_async(empresa_id)
                )
                future.result(timeout=300) 
        except concurrent.futures.TimeoutError:
            print("Timeout ao processar fornecedores")
        except Exception as e:
            print(f"Erro: {e}")
            self.repository.db.rollback()