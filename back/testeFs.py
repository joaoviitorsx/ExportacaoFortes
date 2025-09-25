from src.config.db.conexaoFS import getSessionFS
from src.services.fs.fsExportService import FSExportService

def main():
    session = getSessionFS()
    empresa_id = 1

    service = FSExportService(session)
    cab = service.exportarCAB(empresa_id)
    par = service.exportarPAR(empresa_id)
    pro = service.exportarPRO(empresa_id)
    und = service.exportarUND(empresa_id)
    inm = service.exportarINM(empresa_id)

    #print(cab)
    #print(par)
    #print(pro)
    #print(und)
    print("\n".join(inm))

if __name__ == "__main__":
    main()