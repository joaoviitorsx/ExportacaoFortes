import time
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
        inicio_total = time.time()
        linhas: list[str] = []

        print("[DEBUG] Iniciando exportação CAB")
        t0 = time.time()
        cab = self.exportar.exportarCAB()
        print(f"[DEBUG] CAB exportado em {time.time() - t0:.4f}s")
        if cab:
            linhas.append(cab)

        print("[DEBUG] Iniciando exportação PAR")
        t0 = time.time()
        par = self.exportar.exportarPAR()
        print(f"[DEBUG] PAR exportado em {time.time() - t0:.4f}s")
        linhas.extend(par)

        print("[DEBUG] Iniciando exportação UND")
        t0 = time.time()
        und = self.exportar.exportarUND()
        print(f"[DEBUG] UND exportado em {time.time() - t0:.4f}s")
        linhas.extend(und)

        print("[DEBUG] Iniciando exportação PRO")
        t0 = time.time()
        pro = self.exportar.exportarPRO()
        print(f"[DEBUG] PRO exportado em {time.time() - t0:.4f}s")
        linhas.extend(pro)

        print("[DEBUG] Iniciando exportação NFM")
        t0 = time.time()
        nfm = self.exportar.exportarNFM()
        print(f"[DEBUG] NFM exportado em {time.time() - t0:.4f}s")
        linhas.extend(nfm)

        quantidade_total = len(linhas) + 1
        print(f"[DEBUG] Iniciando builderTRA com {quantidade_total} linhas")
        t0 = time.time()
        tra = builderTRA(quantidade_total)
        print(f"[DEBUG] TRA gerado em {time.time() - t0:.4f}s")
        linhas.append(tra)

        print(f"[DEBUG] Iniciando escrita do arquivo em {self.pathOutput}")
        t0 = time.time()
        with open(self.pathOutput, "w", encoding="latin-1") as f:
            for linha in linhas:
                if linha:
                    f.write(str(linha).strip() + "\n")
        print(f"[DEBUG] Arquivo escrito em {time.time() - t0:.4f}s")

        print(f"[DEBUG] Processo total finalizado em {time.time() - inicio_total:.4f}s")
        return self.pathOutput