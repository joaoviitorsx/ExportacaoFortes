from typing import Dict, Any, List, Optional, Sequence
from sqlalchemy import text
from .builderSNM import builderSNM

class ExportarSNM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 1000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size

    def registros(self, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        """
        Retorna um SNM para cada item (C170) vinculado a uma NFM (C100).
        Cada SNM representa o subtotal daquele produto.
        """
        query = """
            SELECT
                c170.id AS c170_id,
                c170.c100_id,
                c170.vl_item AS vl_opr,
                c170.vl_bc_icms AS vl_bc_icms,
                COALESCE(p.aliquota, c170.aliq_icms) AS aliq_icms,
                c170.vl_icms AS vl_icms,
                c170.vl_ipi AS vl_ipi,
                c170.cst_icms,
                c170.cfop,
                e.simples AS empresa_simples
            FROM registro_c170 AS c170
            JOIN registro_c100 AS c100
                ON c170.c100_id = c100.id
                AND c100.empresa_id = c170.empresa_id
            LEFT JOIN produtos AS p
                ON p.codigo = c170.cod_item
                AND p.empresa_id = c170.empresa_id
            LEFT JOIN empresas AS e
                ON e.id = c100.empresa_id
            WHERE
                c170.empresa_id = :empresa_id
                AND c170.ativo = 1
                AND c100.ativo = 1
        """

        params = {"empresa_id": self.empresa_id}
        if c100_ids:
            query += " AND c100.id IN :c100_ids"
            params["c100_ids"] = tuple(c100_ids)

        query += " ORDER BY c170.c100_id, c170.id"

        rows = self.session.execute(text(query), params).mappings().all()
        return list(rows)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> Dict[int, List[str]]:
        """
        Gera uma linha SNM para cada PNM (item da nota).
        Retorna agrupado por c100_id para facilitar a escrita ordenada.
        """
        registros = self.registros(c100_ids)
        if not registros:
            return {}

        snm_por_nota: Dict[int, List[str]] = {}
        for r in registros:
            c100_id = r["c100_id"]
            linha = builderSNM(r)
            snm_por_nota.setdefault(c100_id, []).append(linha)

        return snm_por_nota

    def gerar_por_nota(self, c100_id: int) -> List[str]:
        """Gera SNMs para uma nota específica."""
        snm_dict = self.gerar([c100_id])
        return snm_dict.get(c100_id, [])
