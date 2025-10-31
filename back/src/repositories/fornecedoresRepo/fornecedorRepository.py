import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

LOTE = 50


class FornecedorRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def novosFornecedores(self, empresa_id: int) -> pd.DataFrame:
        query = text("""
            SELECT cod_part, nome, cnpj
            FROM registro_0150
            WHERE empresa_id = :empresa_id
              AND cnpj IS NOT NULL AND cnpj <> ''
              AND cod_part NOT IN (
                  SELECT cod_part FROM fornecedores WHERE empresa_id = :empresa_id
              )
        """)

        try:
            df = pd.read_sql(query, self.db.bind, params={"empresa_id": empresa_id})
            return df if not df.empty else pd.DataFrame(columns=["cod_part", "nome", "cnpj"])
        except Exception:
            # Em caso de falha no SELECT, não interrompe o fluxo
            return pd.DataFrame(columns=["cod_part", "nome", "cnpj"])

    def inserirFornecedores(self, empresa_id: int, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        df = df.copy()
        df["empresa_id"] = empresa_id
        df["uf"] = ""
        df["cnae"] = ""
        df["decreto"] = ""
        df["simples"] = ""

        colunas = ["empresa_id", "cod_part", "nome", "cnpj", "uf", "cnae", "decreto", "simples"]
        df = df[colunas]

        try:
            df.to_sql(
                name="fornecedores",
                con=self.db.bind,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=1000
            )
            self.db.commit()
            return len(df)
        except Exception:
            self.db.rollback()
            raise

    def cnpjsPendentes(self, empresa_id: int) -> list[str]:
        query = text("""
            SELECT DISTINCT cnpj
            FROM fornecedores
            WHERE empresa_id = :empresa_id
              AND cnpj IS NOT NULL AND cnpj <> ''
              AND (
                  cnae IS NULL OR cnae = '' OR
                  uf IS NULL OR uf = '' OR
                  decreto IS NULL OR decreto = '' OR
                  simples IS NULL OR simples = ''
              )
        """)

        try:
            df = pd.read_sql(query, self.db.bind, params={"empresa_id": empresa_id})
            return df["cnpj"].dropna().tolist()
        except Exception:
            return []
        
    def atualizarFornecedores(self, empresa_id: int, resultados: dict, lote_cnpjs: list[str]):
        if not resultados or not lote_cnpjs:
            return 0

        atualizados = 0
        stmt = text("""
            UPDATE fornecedores
            SET cnae = :cnae,
                uf = :uf,
                simples = :simples,
                decreto = :decreto
            WHERE empresa_id = :empresa_id AND cnpj = :cnpj
        """)

        try:
            for cnpj in lote_cnpjs:
                dados = resultados.get(cnpj)
                if not dados:
                    continue

                razao_social, cnae, uf, simples, decreto = dados
                params = {
                    "empresa_id": empresa_id,
                    "cnpj": cnpj,
                    "cnae": cnae or "",
                    "uf": uf or "",
                    "simples": str(simples or "False"),
                    "decreto": str(decreto or "False")
                }

                self.db.execute(stmt, params)
                atualizados += 1

            self.db.commit()
            return atualizados

        except Exception:
            self.db.rollback()
            raise
