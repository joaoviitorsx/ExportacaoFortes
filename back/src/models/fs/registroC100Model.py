from src.config.db.base import Base

from sqlalchemy import Column, Integer, String, CHAR, DECIMAL, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class RegistroC100(Base):
    __tablename__ = "registro_c100"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), index=True)

    periodo = Column(String(10))
    reg = Column(String(10))
    ind_oper = Column(CHAR(1))
    ind_emit = Column(CHAR(1))
    cod_part = Column(String(60))
    cod_mod = Column(String(10))
    cod_sit = Column(String(10))
    ser = Column(String(10))
    num_doc = Column(String(20))
    chv_nfe = Column(String(60))
    dt_doc = Column(Date)
    dt_e_s = Column(Date)
    vl_doc = Column(DECIMAL(15, 2))
    ind_pgto = Column(String(5))
    vl_desc = Column(DECIMAL(15, 2))
    vl_abat_nt = Column(DECIMAL(15, 2))
    vl_merc = Column(DECIMAL(15, 2))
    ind_frt = Column(String(5))
    vl_frt = Column(DECIMAL(15, 2))
    vl_seg = Column(DECIMAL(15, 2))
    vl_out_da = Column(DECIMAL(15, 2))
    vl_bc_icms = Column(DECIMAL(15, 2))
    vl_icms = Column(DECIMAL(15, 2))
    vl_bc_icms_st = Column(DECIMAL(15, 2))
    vl_icms_st = Column(DECIMAL(15, 2))
    vl_ipi = Column(DECIMAL(15, 2))
    vl_pis = Column(DECIMAL(15, 2))
    vl_cofins = Column(DECIMAL(15, 2))
    vl_pis_st = Column(DECIMAL(15, 2))
    vl_cofins_st = Column(DECIMAL(15, 2))
    filial = Column(String(10))
    ativo = Column(Boolean, default=True)

    itens = relationship("RegistroC170", back_populates="c100")
    totais = relationship("RegistroC190", back_populates="c100")
