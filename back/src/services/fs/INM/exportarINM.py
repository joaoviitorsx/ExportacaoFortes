from collections import defaultdict
from typing import Dict, Any, List, Optional, Sequence
from sqlalchemy import text
from .builderINM import builderINM

class ExportarINM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 1000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size

    def registros(self, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT
                c100.id              AS c100_id,
                c100.cod_part        AS cod_part,
                c100.cod_mod         AS cod_mod,
                p.uf                 AS uf,
                e.simples            AS empresa_simples,

                c170.cfop            AS cfop,
                SUM(c170.vl_item)        AS vl_opr,
                SUM(c170.vl_bc_icms)     AS vl_bc_icms,
                SUM(c170.vl_icms)        AS vl_icms,
                SUM(c170.vl_bc_icms_st)  AS vl_bc_icms_st,
                SUM(c170.vl_icms_st)     AS vl_icms_st,
                SUM(c170.vl_ipi)         AS vl_ipi,
                MAX(c170.cst_icms)       AS cst_icms,
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

        params = {"empresa_id": self.empresa_id}

        if c100_ids:
            query += " AND c100.id IN :c100_ids"
            params["c100_ids"] = tuple(c100_ids)

        query += """
            GROUP BY c100.id, c100.cod_part, c100.cod_mod, p.uf, e.simples, c170.cfop
            ORDER BY c100.id, c170.cfop
        """

        rows = self.session.execute(text(query), params).mappings().all()
        return list(rows)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> List[str]:
        registros = self.registros(c100_ids)
        if not registros:
            return []

        inm_map: Dict[int, List[str]] = defaultdict(list)
        for registro in registros:
            c100_id = registro["c100_id"]
            linha = builderINM(registro)
            inm_map[c100_id].append(linha)

        return dict(inm_map)

    def gerarNota(self, c100_id: int) -> List[str]:
        result = self.gerar([c100_id])
        return result.get(c100_id, [])
