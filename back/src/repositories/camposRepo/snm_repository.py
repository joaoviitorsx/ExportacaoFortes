from typing import Sequence, Dict, Any, List, Optional
from sqlalchemy import text, bindparam

class SnmRepository:
    def __init__(self, session):
        self.session = session

    def get_registros(self, empresa_id: int, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT
                c170.c100_id,
                CAST(COALESCE(p.aliquota, c170.aliq_icms) AS DECIMAL(10,2)) AS aliq_icms,
                SUM(c170.vl_item)      AS vl_opr,
                SUM(c170.vl_bc_icms)   AS vl_bc_icms,
                SUM(c170.vl_icms)      AS vl_icms,
                SUM(c170.vl_ipi)       AS vl_ipi,
                MAX(c170.cst_icms)     AS cst_icms,
                MAX(c170.cfop)         AS cfop,
                MAX(e.simples)         AS empresa_simples,
                MAX(f.decreto)         AS fornecedor_decreto,
                MAX(f.uf)              AS fornecedor_uf
            FROM registro_c170 AS c170
            JOIN registro_c100 AS c100
                ON c170.c100_id = c100.id
                AND c100.empresa_id = c170.empresa_id
                AND c100.ativo = 1
            INNER JOIN produtos AS p
                ON p.codigo = c170.cod_item
                AND p.empresa_id = c170.empresa_id
            INNER JOIN fornecedores AS f
                ON f.cod_part = c100.cod_part
                AND f.empresa_id = c170.empresa_id
            LEFT JOIN empresas AS e
                ON e.id = c100.empresa_id
            WHERE
                c170.empresa_id = :empresa_id
                AND c170.ativo = 1
                AND c100.cod_mod IN ('01', '1B', '04', '55')
                AND c170.cfop IN ('1101', '1401', '1102', '1403', '1910', '1116', '2101', '2102', '2401', '2403', '2910', '2116')
                AND p.aliquota IS NOT NULL 
                AND p.aliquota REGEXP '^[0-9]+\\.[0-9]*$|^[0-9]+$'
                AND CAST(p.aliquota AS DECIMAL(10,2)) > 0
                AND UPPER(TRIM(p.aliquota)) NOT IN ('ST', 'ISENTO')
        """

        params = {"empresa_id": empresa_id}

        if c100_ids:
            query += " AND c100.id IN :c100_ids"
            params["c100_ids"] = list(set(c100_ids))

        query += """
            GROUP BY c170.c100_id, CAST(COALESCE(p.aliquota, c170.aliq_icms) AS DECIMAL(10,2))
            ORDER BY c170.c100_id, CAST(COALESCE(p.aliquota, c170.aliq_icms) AS DECIMAL(10,2))
        """

        if c100_ids:
            stmt = text(query).bindparams(bindparam("c100_ids", expanding=True))
        else:
            stmt = text(query)

        result = self.session.execute(stmt, params).mappings().all()
        return [dict(row) for row in result]