import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
            return pd.DataFrame(columns=["cod_part", "nome", "cnpj"])

    def inserirFornecedores(self, empresa_id: int, df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        df = df.copy()
        df["empresa_id"] = empresa_id
        df["cod_part"] = df["cod_part"].astype(str).str.strip()
        df["uf"] = ""
        df["cnae"] = ""
        df["decreto"] = ""
        df["simples"] = ""

        colunas = ["empresa_id", "cod_part", "nome", "cnpj", "uf", "cnae", "decreto", "simples"]
        df = df[colunas]

        # Usar INSERT IGNORE para pular duplicatas silenciosamente
        stmt = text("""
            INSERT IGNORE INTO fornecedores (empresa_id, cod_part, nome, cnpj, uf, cnae, decreto, simples)
            VALUES (:empresa_id, :cod_part, :nome, :cnpj, :uf, :cnae, :decreto, :simples)
        """)

        try:
            dados = df.to_dict(orient="records")
            
            inseridos = 0
            for registro in dados:
                try:
                    result = self.db.execute(stmt, registro)
                    # rowcount = 1 se inseriu, 0 se foi ignorado (duplicata)
                    if result.rowcount > 0:
                        inseridos += 1
                except IntegrityError:
                    # Se mesmo com INSERT IGNORE houver erro, apenas pula
                    continue
            
            self.db.commit()
            
            total_registros = len(dados)
            ignorados = total_registros - inseridos
            
            if ignorados > 0:
                print(f"[INFO] {inseridos} fornecedores inseridos, {ignorados} duplicados ignorados")
            
            return inseridos
            
        except Exception as e:
            self.db.rollback()
            print(f"[ERRO] Falha ao inserir fornecedores: {e}")
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
            batch_params = []
            for cnpj in lote_cnpjs:
                dados = resultados.get(cnpj)
                if not dados:
                    continue

                razao_social, cnae, uf, simples, decreto = dados
                
                # Garante que CNAE seja string e preserve zeros à esquerda
                cnae_str = str(cnae).zfill(7) if cnae and str(cnae).strip() else ""
                
                params = {
                    "empresa_id": empresa_id,
                    "cnpj": cnpj,
                    "cnae": cnae_str,
                    "uf": uf or "",
                    "simples": str(simples or "False"),
                    "decreto": str(decreto or "False")
                }
                
                batch_params.append(params)

            # Executar em batch
            if batch_params:
                result = self.db.execute(stmt, batch_params)
                atualizados = result.rowcount if hasattr(result, 'rowcount') else len(batch_params)
                self.db.commit()

            return atualizados

        except Exception as e:
            self.db.rollback()
            print(f"[ERRO] Falha ao atualizar fornecedores: {e}")
            raise