from ...services.fs.CAB.exportarCAB import ExportarCAB
from ...services.fs.PAR.exportarPAR import ExportarPAR
from ...services.fs.PRO.exportarPRO import ExportarPRO
from ...services.fs.UND.exportarUND import ExportarUND
from ...services.fs.NFM.exportarNFM import ExportarNFM


class FSExportService:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id    

    def exportarCAB(self) -> str:
        cab = ExportarCAB(self.session).gerar(self.empresa_id)
        return cab

    def exportarPAR(self) -> list[str]:
        par = ExportarPAR(self.session).gerar(self.empresa_id)
        return par or []

    def exportarPRO(self) -> list[str]:
        pro = ExportarPRO(self.session).gerar(self.empresa_id)
        return pro or []

    def exportarUND(self) -> list[str]:
        und = ExportarUND(self.session).gerar(self.empresa_id)
        return und or []

    def exportarNFM(self) -> list[str]:
        nfm = ExportarNFM(self.session, self.empresa_id).gerar()
        return nfm or []
