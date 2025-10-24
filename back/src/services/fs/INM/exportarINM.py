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

                it.vl_opr            AS vl_opr,
                it.vl_bc_icms        AS vl_bc_icms,
                it.vl_icms           AS vl_icms,
                it.vl_bc_icms_st     AS vl_bc_icms_st,
                it.vl_icms_st        AS vl_icms_st,
                it.vl_ipi            AS vl_ipi,
                it.cst_icms          AS cst_icms,
                it.aliq_icms         AS aliq_icms,
                c19.cfop             AS cfop

            FROM registro_c100 AS c100

            -- Totais agregados dos itens (C170)
            JOIN (
                SELECT
                    c170.c100_id,
                    SUM(c170.vl_item)        AS vl_opr,
                    SUM(c170.vl_bc_icms)     AS vl_bc_icms,
                    SUM(c170.vl_icms)        AS vl_icms,
                    SUM(c170.vl_bc_icms_st)  AS vl_bc_icms_st,
                    SUM(c170.vl_icms_st)     AS vl_icms_st,
                    SUM(c170.vl_ipi)         AS vl_ipi,
                    MAX(c170.cst_icms)       AS cst_icms,
                    MAX(c170.aliq_icms)      AS aliq_icms
                FROM registro_c170 c170
                WHERE c170.ativo = 1
                GROUP BY c170.c100_id
            ) AS it ON it.c100_id = c100.id

            -- CFOP representativo (sem multiplicar)
            LEFT JOIN (
                SELECT c190.c100_id, MAX(c190.cfop) AS cfop
                FROM registro_c190 c190
                WHERE c190.ativo = 1
                GROUP BY c190.c100_id
            ) AS c19 ON c19.c100_id = c100.id

            -- Subselect único de registro_0150 (evita múltiplos fornecedores com o mesmo cod_part)
            LEFT JOIN (
                SELECT empresa_id, cod_part, MAX(uf) AS uf
                FROM registro_0150
                WHERE ativo = 1
                GROUP BY empresa_id, cod_part
            ) AS p ON p.cod_part = c100.cod_part AND p.empresa_id = c100.empresa_id

            -- Subselect único da tabela empresas
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

        query += " ORDER BY c100.id"

        rows = self.session.execute(text(query), params).mappings().all()
        return list(rows)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> List[str]:
        """
        Gera 1 linha INM por nota (C100), com totais provenientes de C170.
        """
        registros = self.registros(c100_ids)
        if not registros:
            return []

        linhas_inm: List[str] = []
        for registro in registros:
            # builderINM deve usar os campos agregados (vl_opr, vl_bc_icms, vl_icms, ...).
            linha = builderINM(registro)
            linhas_inm.append(linha)

        return linhas_inm

    def gerar_por_nota(self, c100_id: int) -> List[str]:
        return self.gerar([c100_id])
