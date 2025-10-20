from ...config.db.base import Base

from sqlalchemy import Column, Integer, String, ForeignKey

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), index=True)

    codigo = Column(String(60))
    produto = Column(String(255))
    ncm = Column(String(20))
    aliquota = Column(String(10))
    categoriaFiscal = Column(String(40))
