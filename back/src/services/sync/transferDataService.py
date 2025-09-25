from src.repositories.transfer.empresaRepository import EmpresaRepository
from src.repositories.transfer.produtoRepository import ProdutoRepository

class TransferDataService:
    def __init__(self, sessionICMS, sessionExportacao):
        self.repoEmpresaIcms = EmpresaRepository(sessionICMS)
        self.repoEmpresaExport = EmpresaRepository(sessionExportacao)
        self.repoProdutoIcms = ProdutoRepository(sessionICMS)
        self.repoProdutoExport = ProdutoRepository(sessionExportacao)

    def sincronizarEmpresa(self, empresa_id_destino: int):
        # 1. Buscar empresa no banco exportacao
        empresa_destino = self.repoEmpresaExport.getID(empresa_id_destino)
        if not empresa_destino:
            print("[ERRO] Empresa não encontrada no exportacaofortes.")
            return

        cnpj = empresa_destino["cnpj"]
        empresa_id_export = empresa_destino["id"]

        print(f"[INFO] Empresa destino: {empresa_destino['razao_social']} ({cnpj})")

        # 2. Mapear para empresa no ICMS
        empresa_origem = self.repoEmpresaIcms.getCnpj(cnpj)
        if not empresa_origem:
            print("[ERRO] Empresa não encontrada no apuradoricms.")
            return

        empresa_id_icms = empresa_origem["id"]
        print(f"[INFO] Empresa origem encontrada com ID: {empresa_id_icms}")

        # 3. Buscar produtos do ICMS
        df = self.repoProdutoIcms.getEmpresa(empresa_id_icms)
        if df.empty:
            print("[INFO] Nenhum produto encontrado para transferir.")
            return

        print(f"[INFO] {len(df)} produtos encontrados.")

        # 4. Ajustar para salvar no exportacao
        df["empresa_id"] = empresa_id_export
        # 5. Inserir no exportacao
        self.repoProdutoExport.inserirDados(df)

        print(f"[SUCESSO] {len(df)} produtos transferidos para empresa {empresa_destino['razao_social']}.")
