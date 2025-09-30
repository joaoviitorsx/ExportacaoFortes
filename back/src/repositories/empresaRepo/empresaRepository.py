from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        sql = text("SELECT id, razao_social, cnpj, uf, simples FROM empresas")
        result = self.session.execute(sql).mappings().all()
        return [dict(row) for row in result]

    def insert(self, razao_social: str, cnpj: str, uf: str, simples: bool):
        sql = text("""
            INSERT INTO empresas (razao_social, cnpj, uf, simples)
            VALUES (:razao_social, :cnpj, :uf, :simples)
        """)
        self.session.execute(sql, {
            "razao_social": razao_social,
            "cnpj": cnpj,
            "uf": uf,
            "simples": simples,
        })
        self.session.commit()
        return {"status": "ok"}
