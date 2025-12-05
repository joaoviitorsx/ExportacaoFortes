from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        sql = text("SELECT id, razao_social, cnpj, uf, simples, aliq_espec, cnpj_matriz FROM empresas")
        result = self.session.execute(sql).mappings().all()
        return [dict(row) for row in result]

    def insert(self, razao_social: str, cnpj: str, uf: str, simples: bool, aliq_espec: int = 0, cnpj_matriz: str = None):
        check_sql = text("SELECT id FROM empresas WHERE cnpj = :cnpj")
        exists = self.session.execute(check_sql, {"cnpj": cnpj}).first()

        if exists:
            return {
                "status": "erro", 
                "mensagem": "Empresa já cadastrada."
            }

        # Validar se cnpj_matriz existe quando fornecido
        if cnpj_matriz:
            check_matriz = text("SELECT id FROM empresas WHERE cnpj = :cnpj_matriz")
            matriz_exists = self.session.execute(check_matriz, {"cnpj_matriz": cnpj_matriz}).first()
            
            if not matriz_exists:
                return {
                    "status": "erro",
                    "mensagem": "CNPJ da matriz não encontrado. Cadastre a matriz primeiro."
                }

        sql = text("""
            INSERT INTO empresas (razao_social, cnpj, uf, simples, aliq_espec, cnpj_matriz)
            VALUES (:razao_social, :cnpj, :uf, :simples, :aliq_espec, :cnpj_matriz)
        """)
        self.session.execute(sql, {
            "razao_social": razao_social,
            "cnpj": cnpj,
            "uf": uf,
            "simples": simples,
            "aliq_espec": aliq_espec,
            "cnpj_matriz": cnpj_matriz, 
        })

        self.session.commit()
        return {
            "status": "ok"
        }