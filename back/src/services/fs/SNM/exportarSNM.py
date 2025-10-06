from typing import Dict, Any, List
from sqlalchemy import text
from .builderSNM import builderSNM

class ExportarSNM:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

    def dados(self) -> List[Dict[str, Any]]:
        query = text(
            """
            SELECT DISTINCT
                c190.c100_id,
                c190.vl_opr,
                c190.vl_bc_icms_st,
                COALESCE(p.aliquota, c190.aliq_icms) as aliq_icms,       
                c190.vl_icms_st       
            FROM registro_c190 AS c190
            JOIN registro_c100 AS c100 ON c190.c100_id = c100.id
            LEFT JOIN registro_c170 AS c170 ON c170.c100_id = c100.id
            LEFT JOIN produtos AS p ON p.codigo = c170.cod_item AND p.empresa_id = c170.empresa_id
            WHERE
                c190.empresa_id = :empresa_id;
            """
        )
        result = self.session.execute(query, {"empresa_id": self.empresa_id})
        return list(result.mappings().all())

    def gerar(self) -> Dict[int, List[str]]:
        subtotais = self.dados()
        if not subtotais:
            return {}

        snm: Dict[int, List[str]] = {}
        for dados_subtotal in subtotais:
            c100_id = dados_subtotal["c100_id"]
            if c100_id not in snm:
                snm[c100_id] = []
            
            linha_formatada = builderSNM(dados_subtotal)
            snm[c100_id].append(linha_formatada)
            
        return snm