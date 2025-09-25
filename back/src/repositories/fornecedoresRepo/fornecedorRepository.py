import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

LOTE = 50

class FornecedorRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def novosFornecedores(self, empresa_id: int) -> pd.DataFrame:
        query = text("""
            SELECT r.cod_part, r.nome, r.cnpj
            FROM `registro_0150` r
            WHERE r.empresa_id = :empresa_id
            AND r.cnpj IS NOT NULL AND r.cnpj != ''
            AND r.cod_part NOT IN (
                SELECT cod_part FROM fornecedores WHERE empresa_id = :empresa_id
            )
        """)
        return pd.read_sql(query, self.db.bind, params={"empresa_id": empresa_id})

    def inserirFornecedores(self, empresa_id: int, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        df_insert = df.copy()
        df_insert["empresa_id"] = empresa_id
        df_insert["uf"] = ""
        df_insert["cnae"] = ""
        df_insert["decreto"] = ""
        df_insert["simples"] = ""

        df_insert = df_insert[[
            "empresa_id", "cod_part", "nome", "cnpj", "uf", "cnae", "decreto", "simples"
        ]]

        df_insert.to_sql(
            name="fornecedores",
            con=self.db.bind,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )
        return len(df_insert)

    def cnpjsPendentes(self, empresa_id: int) -> list[str]:
        query = text("""
            SELECT cnpj
            FROM fornecedores
            WHERE empresa_id = :empresa_id
              AND cnpj IS NOT NULL AND cnpj != ''
              AND (
                  cnae IS NULL OR cnae = '' OR
                  uf IS NULL OR uf = '' OR
                  decreto IS NULL OR decreto = '' OR
                  simples IS NULL OR simples = ''
              )
        """)
        df = pd.read_sql(query, self.db.bind, params={"empresa_id": empresa_id})
        return df["cnpj"].drop_duplicates().tolist()

    def atualizarFornecedores(self, empresa_id: int, resultados: dict, lote_cnpjs: list[str]):
        updates = []
        for cnpj in lote_cnpjs:
            dados = resultados.get(cnpj)
            if not dados or all(x is None for x in dados):
                continue
            razao_social, cnae, uf, simples, decreto = dados
            updates.append({
                "cnpj": cnpj,
                "empresa_id": empresa_id,
                "cnae": cnae or '',
                "uf": uf or '',
                "simples": str(simples) if simples is not None else '',
                "decreto": str(decreto) if decreto is not None else ''
            })

        if not updates:
            return

        for row in updates:
            stmt = text("""
                UPDATE fornecedores
                SET cnae = :cnae,
                    uf = :uf,
                    simples = :simples,
                    decreto = :decreto
                WHERE empresa_id = :empresa_id AND cnpj = :cnpj
            """)
            self.db.execute(stmt, row)

        self.db.commit()