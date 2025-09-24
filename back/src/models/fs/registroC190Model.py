from src.config.db.base import Base

from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class RegistroC190(Base):
    __tablename__ = "registro_c190"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), index=True)
    c100_id = Column(Integer, ForeignKey("c100.id"), index=True)

    periodo = Column(String(10), nullable=False)
    reg = Column(String(10), default="C190")
    cst_icms = Column(String(3))
    cfop = Column(String(10))
    aliq_icms = Column(DECIMAL(7, 2))
    vl_opr = Column(DECIMAL(15, 2))
    vl_bc_icms = Column(DECIMAL(15, 2))
    vl_icms = Column(DECIMAL(15, 2))
    vl_bc_icms_st = Column(DECIMAL(15, 2))
    vl_icms_st = Column(DECIMAL(15, 2))
    vl_red_bc = Column(DECIMAL(15, 2))
    vl_ipi = Column(DECIMAL(15, 2))
    cod_obs = Column(String(10))
    ativo = Column(Boolean, default=True)

    c100 = relationship("RegistroC100", back_populates="totais")
