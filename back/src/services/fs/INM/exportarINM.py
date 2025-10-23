from typing import Dict, Any, List, Optional, Sequence
from sqlalchemy import text, bindparam
from .builderINM import builderINM

class ExportarINM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 1000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size

    def registros(self, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT
                c190.id AS c190_id,
                c190.c100_id AS c100_id,
                c190.vl_opr,
                c190.cfop,
                c190.vl_bc_icms,
                c190.aliq_icms,
                c190.vl_icms,
                c190.vl_ipi,
                c190.cst_icms,
                c190.vl_bc_icms_st,
                c190.vl_icms_st,
                p.uf,
                e.simples AS empresa_simples
            FROM registro_c190 AS c190
            JOIN registro_c100 AS c100 
                ON c190.c100_id = c100.id
                AND c100.empresa_id = c190.empresa_id
            LEFT JOIN registro_0150 AS p 
                ON c100.cod_part = p.cod_part 
                AND p.empresa_id = c100.empresa_id
            LEFT JOIN empresas AS e 
                ON c190.empresa_id = e.id
            WHERE c190.empresa_id = :empresa_id
                AND c190.ativo = 1
                AND c100.ativo = 1
        """

        params = {"empresa_id": self.empresa_id}
        if c100_ids:
            query += " AND c190.c100_id IN :c100_ids"
            params["c100_ids"] = tuple(c100_ids)

        query += " ORDER BY c190.c100_id, c190.id"

        rows = self.session.execute(text(query), params).mappings().all()
        return list(rows)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> List[str]:
        #Se c100_ids for informado, gera apenas os INM dessas notas. Caso contrário, gera todos os INM da empresa.

        registros = self.registros(c100_ids)
        if not registros:
            return []

        linhas_inm: List[str] = []
        for registro in registros:
            linha = builderINM(registro)
            linhas_inm.append(linha)

        return linhas_inm

    def gerar_por_nota(self, c100_id: int) -> List[str]:
        #Gera as linhas INM correspondentes a uma única nota fiscal.
        return self.gerar([c100_id])
