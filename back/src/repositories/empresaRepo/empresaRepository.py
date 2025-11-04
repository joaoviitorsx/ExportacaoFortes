from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        sql = text("SELECT id, razao_social, cnpj, uf, simples, aliq_espec FROM empresas")
        result = self.session.execute(sql).mappings().all()
        return [dict(row) for row in result]

    def insert(self, razao_social: str, cnpj: str, uf: str, simples: bool, aliq_espec: int = 0):
        check_sql = text("SELECT id FROM empresas WHERE cnpj = :cnpj")
        exists = self.session.execute(check_sql, {"cnpj": cnpj}).first()

        if exists:
            return {
                "status": "erro", 
                "mensagem": "Empresa já cadastrada."
            }

        sql = text("""
            INSERT INTO empresas (razao_social, cnpj, uf, simples, aliq_espec)
            VALUES (:razao_social, :cnpj, :uf, :simples, :aliq_espec)
        """)
        self.session.execute(sql, {
            "razao_social": razao_social,
            "cnpj": cnpj,
            "uf": uf,
            "simples": simples,
            "aliq_espec": aliq_espec, 
        })

        self.session.commit()
        return {
            "status": "ok"
        }