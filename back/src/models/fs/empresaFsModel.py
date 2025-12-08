from ...config.db.base import Base
from sqlalchemy import Column, Integer, String, CHAR, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class EmpresaFsModel(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(CHAR(14), nullable=False, unique=True, index=True)
    cnpj_raiz = Column(CHAR(8), nullable=False, index=True)
    razao_social = Column(String(100), nullable=False)
    uf = Column(String(2), nullable=False)
    simples = Column(Boolean, nullable=True)
    is_matriz = Column(Boolean, default=False)
    matriz_id = Column(Integer, ForeignKey('empresas.id'), nullable=True, index=True)
    
    # Relacionamentos
    matriz = relationship("EmpresaFsModel", remote_side=[id], backref="filiais")