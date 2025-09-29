from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        sql = text("SELECT id, razao_social, cnpj, uf, simples FROM empresas")
        return self.session.execute(sql).mappings().all()

    def insert(self, razao_social: str, cnpj: str):
        sql = text("""
            INSERT INTO empresas (razao_social, cnpj)
            VALUES (:razao_social, :cnpj)
        """)
        self.session.execute(sql, {"razao_social": razao_social, "cnpj": cnpj})
        self.session.commit()