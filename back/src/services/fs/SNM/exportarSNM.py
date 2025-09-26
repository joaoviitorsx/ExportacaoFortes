from typing import Dict, Any, List
from sqlalchemy import text
from .builderSNM import builderSNM

class ExportarSNM:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

    def subtotais(self) -> List[Dict[str, Any]]:
        query = text(
            """
            SELECT
                c100.num_doc,
                c190.cfop,
                c190.cst_icms,
                c190.aliq_icms,
                c190.vl_opr,
                c190.vl_bc_icms,
                c190.vl_icms,
                c190.vl_bc_icms_st,
                c190.vl_icms_st,
                c190.vl_ipi
            FROM registro_c190 AS c190
            JOIN registro_c100 AS c100 ON c190.c100_id = c100.id
            WHERE
                c190.empresa_id = :empresa_id
            ORDER BY c100.num_doc, c190.cfop, c190.cst_icms;
            """
        )
        
        result = self.session.execute(query, {"empresa_id": self.empresa_id})
        return list(result.mappings().all())

    def gerar(self) -> List[str]:
        subtotais = self.subtotais()
        if not subtotais:
            return []

        linhas_snm: List[str] = []
        for dados_subtotal in subtotais:
            linha_formatada = builderSNM(dados_subtotal)
            linhas_snm.append(linha_formatada)

        return linhas_snm