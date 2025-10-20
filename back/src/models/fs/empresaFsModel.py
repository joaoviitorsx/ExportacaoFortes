from ...config.db.base import Base
from sqlalchemy import Column, Integer, String, CHAR, Boolean

class EmpresaFsModel(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(CHAR(14), nullable=False, unique=True, index=True)
    razao_social = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)
    simples = Column(Boolean, nullable=True)