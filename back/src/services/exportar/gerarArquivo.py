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
        linhas: list[str] = []

        cab = self.exportar.exportarCAB()
        if cab:
            linhas.append(cab)

        par = self.exportar.exportarPAR()
        linhas.extend(par)

        und = self.exportar.exportarUND()
        linhas.extend(und)

        pro = self.exportar.exportarPRO()
        linhas.extend(pro)

        nfm = self.exportar.exportarNFM()
        linhas.extend(nfm)

        quantidade_total = len(linhas) + 1
        tra = builderTRA(quantidade_total)
        linhas.append(tra)

        with open(self.pathOutput, "w", encoding="latin-1") as f:
            for linha in linhas:
                if linha:
                    f.write(str(linha).strip() + "\n")

        return self.pathOutput
