from config.db.base import Base


from sqlalchemy import Column, Integer, String, ForeignKey

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), index=True)

    cod_part = Column(String(60))
    nome = Column(String(100))
    cnpj = Column(String(20))
    uf = Column(String(5))
    cnae = Column(String(20))
    decreto = Column(String(10))
    simples = Column(String(10))
