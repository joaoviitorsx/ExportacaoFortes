from typing import List, Dict, Any
from sqlalchemy import text

class NFMRepository:
    def __init__(self, session):
        self.session = session

    def get_notas(self, empresa_id: int) -> List[Dict[str, Any]]:
        query = text("""
                SELECT
                    c.id AS c100_id,
                    c.ind_oper, c.ind_emit, c.cod_part, c.cod_mod, c.cod_sit, c.ser,
                    c.num_doc, c.chv_nfe, c.dt_doc, c.dt_e_s, c.vl_doc, c.ind_pgto,
                    c.vl_desc, c.vl_merc, c.ind_frt, c.vl_frt, c.vl_seg, c.vl_out_da,
                    c.vl_bc_icms, c.vl_icms, c.vl_bc_icms_st, c.vl_icms_st, c.vl_ipi,
                    c.vl_pis, c.vl_cofins,
                    r0.filial AS estabelecimento,
                    COUNT(DISTINCT c170.id) AS qtd_itens
                FROM registro_c100 AS c

                JOIN registro_0000 AS r0 
                    ON r0.empresa_id = c.empresa_id 
                    AND r0.ativo = 1

                JOIN registro_c170 AS c170
                    ON c170.c100_id = c.id
                    AND c170.ativo = 1

                LEFT JOIN registro_c190 AS c190
                    ON c190.c100_id = c.id
                    AND c190.ativo = 1

                WHERE
                    c.empresa_id = :empresa_id
                    AND c.ativo = 1

                GROUP BY
                    c.id, c.ind_oper, c.ind_emit, c.cod_part, c.cod_mod, c.cod_sit, c.ser,
                    c.num_doc, c.chv_nfe, c.dt_doc, c.dt_e_s, c.vl_doc, c.ind_pgto,
                    c.vl_desc, c.vl_merc, c.ind_frt, c.vl_frt, c.vl_seg, c.vl_out_da,
                    c.vl_bc_icms, c.vl_icms, c.vl_bc_icms_st, c.vl_icms_st, c.vl_ipi,
                    c.vl_pis, c.vl_cofins, r0.filial

                ORDER BY c.dt_doc, c.num_doc
            """)

        result = self.session.execute(query, {"empresa_id": empresa_id}).mappings().all()
        return [dict(row) for row in result]