from ...repositories.transferRepo.empresaRepository import EmpresaRepository
from ...repositories.transferRepo.produtoRepository import ProdutoRepository
from ...services.sync.validacaoTransferService import ValidacaoTransferService

class TransferDataService:
    def __init__(self, sessionICMS, sessionExportacao):
        self.repoEmpresaIcms = EmpresaRepository(sessionICMS)
        self.repoEmpresaExport = EmpresaRepository(sessionExportacao)
        self.repoProdutoIcms = ProdutoRepository(sessionICMS)
        self.repoProdutoExport = ProdutoRepository(sessionExportacao)
        self.validador = ValidacaoTransferService()

    def sincronizarEmpresa(self, empresaIdDestino: int):
        # 1. Buscar empresa no banco exportacao
        empresaDestino = self.repoEmpresaExport.getID(empresaIdDestino)
        if not empresaDestino:
            print("[ERRO] Empresa não encontrada no banco exportacaofortes.")
            return

        cnpj = empresaDestino["cnpj"]
        empresaIdExport = empresaDestino["id"]

        print(f"[INFO] Empresa destino: {empresaDestino['razao_social']} ({cnpj})")

        # 2. Mapear para empresa no ICMS
        empresaOrigem = self.repoEmpresaIcms.getCnpj(cnpj)
        if not empresaOrigem:
            print("[ERRO] Empresa não encontrada no apuradoricms.")
            return

        empresa_id_icms = empresaOrigem["id"]
        print(f"[INFO] Empresa origem encontrada com ID: {empresa_id_icms}")

        # 3. Buscar produtos do ICMS
        df = self.repoProdutoIcms.getEmpresa(empresa_id_icms)
        if df.empty:
            print("[INFO] Nenhum produto encontrado para transferir.")
            return

        print(f"[INFO] {len(df)} produtos encontrados.")

        dfValidado = self.validador.validar(df)
        if dfValidado.empty:
            print("[ERRO] Nenhum dado válido para transferir após validação.")
            return
        
        # 4. Ajustar para salvar no exportacao
        df["empresa_id"] = empresaIdExport
        self.repoProdutoExport.inserirDados(df)

        print(f"[SUCESSO] {len(df)} produtos transferidos para empresa {empresaDestino['razao_social']}.")
