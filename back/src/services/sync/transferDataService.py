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
        is_matriz = bool(empresaDestino.get("is_matriz", False))
        matriz_id = empresaDestino.get("matriz_id") or empresaDestino["id"]
        empresaIdExport = empresaDestino["id"]

        print(f"[INFO] Empresa destino: {empresaDestino['razao_social']} ({cnpj})")

        # 2. Determinar CNPJ para buscar produtos (sempre da matriz)
        if is_matriz:
            cnpj_busca = cnpj
            print(f"[INFO] Empresa é MATRIZ. Buscando produtos próprios.")
        else:
            matriz = self.repoEmpresaExport.getID(matriz_id)
            if not matriz:
                print(f"[ERRO] Matriz não encontrada (ID: {matriz_id}).")
                return

            cnpj_busca = matriz["cnpj"]
            print(f"[INFO] Empresa é FILIAL. Buscando produtos da matriz: {cnpj_busca}")

        # 3. Mapear para empresa no ICMS
        empresaOrigem = self.repoEmpresaIcms.getCnpj(cnpj_busca)
        if not empresaOrigem:
            print(f"[ERRO] Empresa com CNPJ {cnpj_busca} não encontrada no apuradoricms.")
            return

        empresa_id_icms = empresaOrigem["id"]
        print(f"[INFO] Empresa origem encontrada com ID: {empresa_id_icms}")

        # 4. Buscar produtos do ICMS
        df = self.repoProdutoIcms.getEmpresa(empresa_id_icms)
        if df.empty:
            print("[INFO] Nenhum produto encontrado para transferir.")
            return

        print(f"[INFO] {len(df)} produtos encontrados.")

        # 5. Validar dados
        dfValidado = self.validador.validar(df)
        if dfValidado.empty:
            print("[ERRO] Nenhum dado válido para transferir após validação.")
            return
        
        # 6. Determinar empresa_id para gravar produtos
        # REGRA: Filiais usam empresa_id da MATRIZ para compartilhar produtos
        if is_matriz:
            empresa_id_produtos = empresaIdExport  # Matriz usa próprio ID
            print(f"[INFO] Gravando produtos com empresa_id da MATRIZ: {empresa_id_produtos}")
        else:
            empresa_id_produtos = matriz_id  # Filial usa ID da matriz
            print(f"[INFO] Gravando produtos com empresa_id da MATRIZ (filial compartilha): {empresa_id_produtos}")
        
        # 7. Sincronizar produtos (INSERT + UPDATE)
        dfValidado["empresa_id"] = empresa_id_produtos
        self.repoProdutoExport.inserirDados(dfValidado, empresa_id_produtos)

        tipo = "matriz" if is_matriz else "filial"
        print(f"[SUCESSO] Produtos sincronizados para {tipo} {empresaDestino['razao_social']}.")
