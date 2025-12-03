from sqlalchemy import text

class ParRepository:
    def __init__(self, session):
        self.session = session

    def get_registros_0150(self, empresa_id: int):
        query = text("""
            SELECT cod_part, nome, uf, cnpj, cpf, ie,
                   ende, num, compl, bairro,
                   cod_mun, suframa, cod_pais
            FROM registro_0150
            WHERE empresa_id = :empresa_id 
              AND ativo = 1
        """)
        return self.session.execute(query, {"empresa_id": empresa_id}).mappings().all()
    
    def get_fornecedores(self, empresa_id: int):
        query = text("""
            SELECT cod_part, nome, cnpj, uf, cnae, simples
            FROM fornecedores
            WHERE empresa_id = :empresa_id
        """)
        return self.session.execute(query, {"empresa_id": empresa_id}).mappings().all()
