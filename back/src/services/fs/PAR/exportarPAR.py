from ....services.fs.PAR.builderPAR import builderPAR
from ....repositories.camposRepo.par_repository import ParRepository

class ExportarPAR:
    def __init__(self, session):
        self.session = session
        self.repo = ParRepository(session)

    def gerar(self, empresa_id: int) -> list[str]:
        registros_0150 = self.repo.get_registros_0150(empresa_id)

        if not registros_0150:
            raise ValueError("Nenhum registro 0150 encontrado para a empresa.")

        fornecedores = self.repo.get_fornecedores(empresa_id)

        mapa_forn = {f["cod_part"]: f for f in fornecedores}

        linhas_par = []

        for reg in registros_0150:
            cod_part = reg["cod_part"]
            dados = dict(reg)

            if cod_part in mapa_forn:
                dados.update(mapa_forn[cod_part])

            linha = builderPAR(dados)
            linhas_par.append(linha)

        return linhas_par
