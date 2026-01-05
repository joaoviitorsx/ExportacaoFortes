from typing import Dict, List
from .builderOUM import builderOUM
from ....repositories.camposRepo.oum_repository import OumRepository

class ExportarOUM:
    def __init__(self, session):
        self.session = session
        self.repo = OumRepository(session)

    def gerar(self, produtos: list[dict], empresa_id: int) -> dict[str, list[str]]:
        mapa_db = self.repo.get_oum(empresa_id)
        resultado: dict[str, list[str]] = {}

        produtos_por_item: dict[str, dict] = {}

        for p in produtos:
            cod_item = p.get("cod_item")
            if cod_item not in produtos_por_item:
                produtos_por_item[cod_item] = p

        for cod_item, prod in produtos_por_item.items():
            unid_padrao = prod.get("unid_inv")

            linhas = []
            unidades_geradas = set()

            # OUM padrão (sempre 1)
            linhas.append(
                builderOUM({
                    "cod_item": cod_item,
                    "unid_conv": unid_padrao,
                    "fat_conv": 0.0
                })
            )

            unidades_geradas.add(unid_padrao)

            # OUMs alternativos (0220)
            for r in mapa_db.get(cod_item, []):
                unid_conv = r["unid_conv"]
                fat_conv = float(r["fat_conv"] or 0)

                # ignora conversão inútil
                if unid_conv == unid_padrao and fat_conv == 1:
                    continue

                # garante unicidade absoluta
                if unid_conv in unidades_geradas:
                    continue

                unidades_geradas.add(unid_conv)

                linhas.append(
                    builderOUM({
                        "cod_item": cod_item,
                        "unid_conv": unid_conv,
                        "fat_conv": fat_conv
                    })
                )

            resultado[cod_item] = linhas

        return resultado
