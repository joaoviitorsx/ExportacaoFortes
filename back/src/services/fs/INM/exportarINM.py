from typing import Dict, Any, List
from sqlalchemy import text
from .builderINM import builderINM

class ExportarINM:
    def __init__(self, session):
        self.session = session

    def gerar(self, empresa_id: int) -> List[str]:
        query = text("""
            SELECT
                c190.vl_opr,
                c190.cfop,
                c190.vl_bc_icms,
                c190.aliq_icms,
                c190.vl_icms,
                c190.vl_ipi,
                c190.cst_icms,
                c190.vl_bc_icms_st,
                c190.vl_icms_st,
                p.uf,
                e.simples AS empresa_simples
            FROM registro_c190 AS c190
            JOIN registro_c100 AS c100 ON c190.c100_id = c100.id
            LEFT JOIN registro_0150 AS p ON c100.cod_part = p.cod_part AND p.empresa_id = c100.empresa_id
            LEFT JOIN empresas AS e ON c190.empresa_id = e.id
            WHERE c190.empresa_id = :empresa_id
        """)
        
        result = self.session.execute(query, {"empresa_id": empresa_id})
        
        linhas_inm = []
        for registro_agregado in result.mappings().all():
            linhas_inm.append(builderINM(registro_agregado))
            
        return linhas_inm