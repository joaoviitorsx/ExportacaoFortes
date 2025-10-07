from ...services.fs.CAB.exportarCAB import ExportarCAB
from ...services.fs.PAR.exportarPAR import ExportarPAR
from ...services.fs.PRO.exportarPRO import ExportarPRO
from ...services.fs.UND.exportarUND import ExportarUND
from ...services.fs.PNM.exportarPNM import ExportarPNM
from ...services.fs.INM.exportarINM import ExportarINM
from ...services.fs.NFM.exportarNFM import ExportarNFM
from ...services.fs.SNM.exportarSNM import ExportarSNM

class FSExportService:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id    

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
    
    def exportarNFM(self, empresa_id: int):
        nfm = ExportarNFM(self.session, empresa_id).gerar()
        return nfm
    
    def exportarSNM(self, empresa_id: int):
        snm = ExportarSNM(self.session, empresa_id).gerar()
        return snm
    
    def exportarINM(self, empresa_id: int):
        inm = ExportarINM(self.session).gerar(empresa_id)
        return inm