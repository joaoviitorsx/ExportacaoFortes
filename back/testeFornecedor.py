from src.config.db.conexaoFS import getSessionFS
from src.repositories.fornecedoresRepo.fornecedorRepository import FornecedorRepository
from src.services.fornecedor.fornecedorService import FornecedorService

def main():
    empresa_id = 1  

    session = getSessionFS()

    repo = FornecedorRepository(session)
    service = FornecedorService(repo)

    print("busca fornecedores")
    service.processar(empresa_id)

if __name__ == "__main__":
    main()
