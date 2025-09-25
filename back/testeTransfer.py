from src.config.db.conexaoICMS import getSessionICMS
from src.config.db.conexaoFS import getSessionFS
from src.services.sync.transferDataService import TransferDataService

# Criar sessões
sessionICMS = getSessionICMS()
sessionExportacao = getSessionFS()

# Rodar serviço
transfer = TransferDataService(sessionICMS, sessionExportacao)
transfer.sincronizarEmpresa(empresaIdDestino=1)