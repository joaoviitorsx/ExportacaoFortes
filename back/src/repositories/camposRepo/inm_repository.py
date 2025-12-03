from typing import Sequence, Dict, Any, List, Optional
from sqlalchemy import text, bindparam

class InmRepository:
    def __init__(self, session):
        self.session = session

    def get_registros(self, empresa_id: int, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT
                c100.id              AS c100_id,
                c100.cod_part        AS cod_part,
                c100.cod_mod         AS cod_mod,
                p.uf                 AS uf,
                e.simples            AS empresa_simples,
                c170.cfop            AS cfop,
                c170.cst_icms        AS cst_icms,
                SUM(c170.vl_item)        AS vl_opr,
                SUM(c170.vl_bc_icms)     AS vl_bc_icms,
                SUM(c170.vl_icms)        AS vl_icms,
                SUM(c170.vl_bc_icms_st)  AS vl_bc_icms_st,
                SUM(c170.vl_icms_st)     AS vl_icms_st,
                SUM(c170.vl_ipi)         AS vl_ipi,
                MAX(c170.aliq_icms)      AS aliq_icms
            FROM registro_c100 AS c100
            JOIN registro_c170 c170
                ON c170.c100_id = c100.id
                AND c170.ativo = 1
            LEFT JOIN (
                SELECT empresa_id, cod_part, MAX(uf) AS uf
                FROM registro_0150
                WHERE ativo = 1
                GROUP BY empresa_id, cod_part
            ) AS p ON p.cod_part = c100.cod_part AND p.empresa_id = c100.empresa_id
            LEFT JOIN (
                SELECT id, MAX(simples) AS simples
                FROM empresas
                GROUP BY id
            ) AS e ON e.id = c100.empresa_id
            WHERE
                c100.empresa_id = :empresa_id
                AND c100.ativo = 1
        """

        params = {"empresa_id": empresa_id}

        if c100_ids:
            query += " AND c100.id IN :c100_ids"
            params["c100_ids"] = list(set(c100_ids))

        query += """
            GROUP BY c100.id, c100.cod_part, c100.cod_mod, p.uf, e.simples, c170.cfop, c170.cst_icms
            ORDER BY c100.id, c170.cfop, c170.cst_icms
        """

        if c100_ids:
            stmt = text(query).bindparams(bindparam("c100_ids", expanding=True))
        else:
            stmt = text(query)

        result = self.session.execute(stmt, params).mappings().all()
        return [dict(row) for row in result]