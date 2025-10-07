from ....src.config.db.conexaoFS import getSessionFS
from ....src.services.fs.TRA.builderTRA import builderTRA
from ....src.services.fs.fsExportService import FSExportService
from ...utils.fsFormat import normalizarDados

class GerarArquivo:
    def __init__(self, empresa_id: int, pathOutput: str):
        self.session = getSessionFS()
        self.empresa_id = empresa_id
        self.pathOutput = pathOutput
        self.exportar = FSExportService(self.session, self.empresa_id)

    def gerar(self) -> str:
        linhas = []

        cab = self.exportar.exportarCAB(self.empresa_id)
        if cab:
            linhas.append(cab)

        par = self.exportar.exportarPAR(self.empresa_id)
        if par:
            linhas.extend(par)

        und = self.exportar.exportarUND(self.empresa_id)
        if und:
            linhas.extend(und)

        pro = self.exportar.exportarPRO(self.empresa_id)
        if pro:
            linhas.extend(pro)

        nfm = self.exportar.exportarNFM(self.empresa_id)
        if nfm:
            linhas.extend(nfm)

        pnm = self.exportar.exportarPNM(self.empresa_id)
        if pnm:
            linhas.extend(pnm)

        snm = self.exportar.exportarSNM(self.empresa_id)
        if snm:
            if isinstance(snm, dict):
                snm_linhas = []
                for lista in snm.values():
                    if isinstance(lista, list):
                        snm_linhas.extend(lista)
                    elif isinstance(lista, str):
                        snm_linhas.append(lista)
                linhas.extend(snm_linhas)
            elif isinstance(snm, list):
                linhas.extend(snm)

        inm = self.exportar.exportarINM(self.empresa_id)
        if inm:
            linhas.extend(inm)

        quantidade_total = len(linhas) + 1
        tra = builderTRA(quantidade_total)
        linhas.append(tra)

        with open(self.pathOutput, "w", encoding="latin-1") as f:
            for linha in linhas:
                if linha:
                    f.write(str(linha).strip() + "\n")

        return self.pathOutput