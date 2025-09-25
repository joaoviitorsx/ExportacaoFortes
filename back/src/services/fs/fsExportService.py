from src.services.fs.CAB.exportarCAB import ExportarCAB
from src.services.fs.PAR.exportarPAR import ExportarPAR
from src.services.fs.PRO.exportarPRO import ExportarPRO
from src.services.fs.UND.exportarUND import ExportarUND
from src.services.fs.PNM.exportarPNM import ExportarPNM
from src.services.fs.INM.exportarINM import ExportarINM

class FSExportService:
    def __init__(self, session):
        self.session = session

    def exportarCAB(self, empresa_id: int):
        cab = ExportarCAB(self.session).gerar(empresa_id)
        return cab
    
    def exportarPAR(self, empresa_id: int):
        par = ExportarPAR(self.session).gerar(empresa_id)
        return par
    
    def exportarPRO(self, empresa_id: int):
        pro = ExportarPRO(self.session).gerar(empresa_id)
        return pro
    
    def exportarUND(self, empresa_id: int):
        und = ExportarUND(self.session).gerar(empresa_id)
        return und
    
    def exportarPNM(self, empresa_id: int):
        pnm = ExportarPNM(self.session, empresa_id).gerar()
        return pnm
    
    def exportarINM(self, empresa_id: int):
        inm = ExportarINM(self.session).gerar(empresa_id)
        return inm