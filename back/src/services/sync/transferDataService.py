from src.repositories.transfer.empresaRepository import EmpresaRepository
from src.repositories.transfer.produtoRepository import ProdutoRepository

class TransferDataService:
    def __init__(self, sessionICMS, sessionExportacao):
        self.repo_empresa_icms = EmpresaRepository(sessionICMS)
        self.repo_empresa_export = EmpresaRepository(sessionExportacao)
        self.repo_produto_icms = ProdutoRepository(sessionICMS)
        self.repo_produto_export = ProdutoRepository(sessionExportacao)

    def sincronizarEmpresa(self, empresa_id_destino: int):
        # 1. Buscar empresa no banco exportacao
        empresa_destino = self.repo_empresa_export.getId(empresa_id_destino)
        if not empresa_destino:
            print("[ERRO] Empresa não encontrada no exportacaofortes.")
            return

        cnpj = empresa_destino["cnpj"]
        empresa_id_export = empresa_destino["empresa_id"]

        print(f"[INFO] Empresa destino: {empresa_destino['razaoSocial']} ({cnpj})")

        # 2. Mapear para empresa no ICMS
        empresa_origem = self.repo_empresa_icms.getCnpj(cnpj)
        if not empresa_origem:
            print("[ERRO] Empresa não encontrada no apuradoricms.")
            return

        empresa_id_icms = empresa_origem["empresa_id"]
        print(f"[INFO] Empresa origem encontrada com ID: {empresa_id_icms}")

        # 3. Buscar produtos do ICMS
        df = self.repo_produto_icms.getEmpresa(empresa_id_icms)
        if df.empty:
            print("[INFO] Nenhum produto encontrado para transferir.")
            return

        print(f"[INFO] {len(df)} produtos encontrados.")

        # 4. Ajustar para salvar no exportacao
        df["empresa_id"] = empresa_id_export

        # 5. Inserir no exportacao
        self.repo_produto_export.inserirDados(df)

        print(f"[SUCESSO] {len(df)} produtos transferidos para empresa {empresa_destino['razaoSocial']}.")
