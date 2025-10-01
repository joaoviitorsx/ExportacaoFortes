from typing import Dict, Any, List
from sqlalchemy import text
from .builderSNM import builderSNM

class ExportarSNM:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

    def subtotais_st(self) -> List[Dict[str, Any]]:
        query = text(
            """
            SELECT
                c190.c100_id,
                c190.vl_opr,
                c190.vl_bc_icms_st,  -- Campo correto para a Base de Cálculo
                c190.aliq_icms,       -- Usado para a alíquota (verificar se é a alíquota interna correta)
                c190.vl_icms_st       -- Pode ser útil para o campo "Já Recolhido", dependendo da regra
            FROM registro_c190 AS c190
            JOIN registro_c100 AS c100 ON c190.c100_id = c100.id
            WHERE
                c190.empresa_id = :empresa_id
                AND c100.ind_oper = '0'
                AND c190.vl_icms_st > 0;
            """
        )
        result = self.session.execute(query, {"empresa_id": self.empresa_id})
        return list(result.mappings().all())

    def gerar(self) -> Dict[int, List[str]]:
        subtotais = self.subtotais_st()
        if not subtotais:
            return {}

        snm_por_nota: Dict[int, List[str]] = {}
        for dados_subtotal in subtotais:
            c100_id = dados_subtotal["c100_id"]
            if c100_id not in snm_por_nota:
                snm_por_nota[c100_id] = []
            
            linha_formatada = builderSNM(dados_subtotal)
            snm_por_nota[c100_id].append(linha_formatada)
            
        return snm_por_nota