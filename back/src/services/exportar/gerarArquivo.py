from ....src.config.db.conexaoFS import getSessionFS
from ....src.services.fs.TRA.builderTRA import builderTRA
from ....src.services.fs.fsExportService import FSExportService

class GerarArquivo:
    def __init__(self, empresa_id: int, pathOutput: str):
        self.session = getSessionFS()
        self.empresa_id = empresa_id
        self.pathOutput = pathOutput
        self.exportar = FSExportService(self.session, self.empresa_id)

    def gerar(self) -> str:
        linhas = []
        linhas.append(self.exportar.exportarCAB(self.empresa_id))
        linhas.extend(self.exportar.exportarPAR(self.empresa_id))
        linhas.extend(self.exportar.exportarUND(self.empresa_id))
        linhas.extend(self.exportar.exportarPRO(self.empresa_id))
        linhas.extend(self.exportar.exportarNFM(self.empresa_id))
        linhas.extend(self.exportar.exportarPNM(self.empresa_id))
        linhas.extend(self.exportar.exportarSNM(self.empresa_id))
        linhas.extend(self.exportar.exportarINM(self.empresa_id))

        quantidade_total = len(linhas) + 1
        tra = builderTRA(quantidade_total)
        linhas.append(tra)

        with open(self.pathOutput, "w", encoding="latin-1") as f:
            for linha in linhas:
                f.write(linha.strip() + "\n")

        print(f"Arquivo gerado em: {self.pathOutput}")
        return self.pathOutput
