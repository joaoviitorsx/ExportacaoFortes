from sqlalchemy import text
from ....services.fs.PAR.builderPAR import builderPAR

class ExportarPAR:
    def __init__(self, session):
        self.session = session

    def gerar(self, empresa_id: int) -> list[str]:
        registros_0150 = self.session.execute(
            text("""
                SELECT cod_part, nome, uf, cnpj, cpf, ie,
                       ende, num, compl, bairro,
                       cod_mun, suframa, cod_pais
                FROM registro_0150
                WHERE empresa_id = :empresa_id 
                  AND ativo = 1
            """),
            {"empresa_id": empresa_id}
        ).mappings().all()

        if not registros_0150:
            raise ValueError("Nenhum registro 0150 encontrado para a empresa.")

        fornecedores = self.session.execute(
            text("""
                SELECT cod_part, nome, cnpj, uf, cnae, simples
                FROM fornecedores
                WHERE empresa_id = :empresa_id
            """),
            {"empresa_id": empresa_id}
        ).mappings().all()

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
