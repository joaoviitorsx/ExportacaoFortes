from sqlalchemy import text
from ....services.fs.CAB.builderCAB import builderCAB

class ExportarCAB:
    def __init__(self, session):
        self.session = session

    def gerar(self, empresa_id: int) -> str:
        # Buscar empresa
        empresa = self.session.execute(
            text("SELECT razao_social, aliq_espec FROM empresas WHERE id = :id"),
            {"id": empresa_id}
        ).mappings().first()

        # Buscar registro 0000
        registro_0000 = self.session.execute(
            text("SELECT dt_ini, dt_fin, periodo FROM registro_0000 WHERE empresa_id = :id AND ativo = 1 LIMIT 1"),
            {"id": empresa_id}
        ).mappings().first()

        if not empresa or not registro_0000:
            raise ValueError("Dados insuficientes para gerar CAB")

        return builderCAB(empresa, registro_0000)
