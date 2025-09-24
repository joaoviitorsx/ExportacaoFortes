from src.config.db.conexaoFS import getSessionFS
from src.services.etl.pipelineService import PipelineService

if __name__ == "__main__":
    session = getSessionFS()
    empresa_id = 1
    arquivos = [
        r"C:\Users\joaov\OneDrive\Documentos\Estagio\documentacao\EFD 07.2025\FL 02 - SPED FISCAL 07.2025.txt",
        r"C:\Users\joaov\OneDrive\Documentos\Estagio\documentacao\EFD 07.2025\FL 03 - SPED FISCAL 07.2025.txt",
        r"C:\Users\joaov\OneDrive\Documentos\Estagio\documentacao\EFD 07.2025\FL 04 - SPED FISCAL 07.2025.txt",
        r"C:\Users\joaov\OneDrive\Documentos\Estagio\documentacao\EFD 07.2025\FL 05 - SPED FISCAL 07.2025.txt",
        r"C:\Users\joaov\OneDrive\Documentos\Estagio\documentacao\EFD 07.2025\FL 06 - SPED FISCAL 07.2025.txt",
        r"C:\Users\joaov\OneDrive\Documentos\Estagio\documentacao\EFD 07.2025\MTZ - SPED FISCAL 07.2025.2025.txt",
    ]

    pipeline = PipelineService(session, empresa_id, arquivos, num_workers=2, buffer_size=5000)
    pipeline.executar()
