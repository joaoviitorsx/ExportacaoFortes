from typing import Dict, Any, List, Optional, Sequence
from sqlalchemy import text, bindparam
from .builderSNM import builderSNM

class ExportarSNM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 1000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size

    def dados(self, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT DISTINCT
                c190.c100_id,
                c190.vl_opr,
                c190.vl_bc_icms_st,
                COALESCE(p.aliquota, c190.aliq_icms) AS aliq_icms,
                c190.vl_icms_st
            FROM registro_c190 AS c190
            JOIN registro_c100 AS c100
                ON c190.c100_id = c100.id
            LEFT JOIN registro_c170 AS c170
                ON c170.c100_id = c100.id
            LEFT JOIN produtos AS p
                ON p.codigo = c170.cod_item
               AND p.empresa_id = c170.empresa_id
            WHERE
                c190.empresa_id = :empresa_id
                AND c190.ativo = 1
                AND c100.ativo = 1
                AND (c170.ativo = 1 OR c170.ativo IS NULL)
        """

        params = {"empresa_id": self.empresa_id}
        if c100_ids:
            query += " AND c190.c100_id IN :c100_ids"
            params["c100_ids"] = tuple(c100_ids)

        query += " ORDER BY c190.c100_id"

        rows = self.session.execute(text(query), params).mappings().all()
        return list(rows)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> List[str]:
        #Se c100_ids for informado, gera apenas os SNM dessas notas.Caso contrário, gera todos os SNM da empresa.
        subtotais = self.dados(c100_ids)
        if not subtotais:
            return []

        linhas_snm: List[str] = []
        for subtotal in subtotais:
            linha_formatada = builderSNM(subtotal)
            linhas_snm.append(linha_formatada)

        return linhas_snm

    def gerar_por_nota(self, c100_id: int) -> List[str]:
        #Gera as linhas SNM correspondentes a uma única nota fiscal.
        return self.gerar([c100_id])
