import asyncio
from src.utils.cnpj import processarCnpjs
from src.repositories.fornecedoresRepo.fornecedorRepository import FornecedorRepository

LOTE = 50

class FornecedorService:
    def __init__(self, repository: FornecedorRepository):
        self.repository = repository

    def processar(self, empresa_id: int):
        try:
            print("Buscando fornecedores novos para inserção...")
            df_novos = self.repository.novosFornecedores(empresa_id)
            print(f"Novos fornecedores encontrados: {len(df_novos)}")
            inseridos = self.repository.inserirFornecedores(empresa_id, df_novos)
            print(f"{inseridos} fornecedores inseridos.")

            print("Atualizando fornecedores com dados externos...")
            cnpjs = self.repository.cnpjsPendentes(empresa_id)
            print(f"CNPJs pendentes: {len(cnpjs)}")

            if not cnpjs:
                print("Nenhum CNPJ pendente de atualização.")
                return

            print(f"Consultando API externa para {len(cnpjs)} CNPJs...")
            resultados = asyncio.run(processarCnpjs(cnpjs))

            print("Atualizando cadastro_fornecedores")
            for i in range(0, len(cnpjs), LOTE):
                batch = cnpjs[i:i + LOTE]
                self.repository.atualizarFornecedores(empresa_id, resultados, batch)
                print(f"✅ Lote de {len(batch)} CNPJs atualizado.")

            print("Atualização finalizada com sucesso.")

        except Exception as e:
            self.repository.db.rollback()
            print(f"[ERRO] Falha na atualização de fornecedores: {e}")