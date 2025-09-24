from sqlalchemy import text

class EmpresaRepository:
    def __init__(self, session):
        self.session = session

    def getId(self, empresa_id: int):
        query = text("SELECT empresa_id, cnpj, razaoSocial FROM empresas WHERE empresa_id = :id")
        return self.session.execute(query, {"id": empresa_id}).mappings().first()

    def getCnpj(self, cnpj: str):
        query = text("SELECT empresa_id, cnpj, razaoSocial FROM empresas WHERE cnpj = :cnpj")
        return self.session.execute(query, {"cnpj": cnpj}).mappings().first()
