from ....services.fs.UND.builderUND import builderUND
from ....repositories.camposRepo.und_repository import UndRepository


class ExportarUND:
    def __init__(self, session):
        self.session = session
        self.repo = UndRepository(session)

    def gerar(self, empresa_id: int) -> list[str]:
        unidades = self.repo.listar_unidades(empresa_id)

        if not unidades:
            return []

        linhas = []
        for u in unidades:
            linhas.append(
                builderUND(
                    cod_unid=u["unid"],
                    descr_unid=u["descr"]
                )
            )

        return linhas
