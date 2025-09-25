from sqlalchemy import text
from src.services.fs.INM.builderINM import builderINM

class ExportarINM:
    def __init__(self, session):
        self.session = session

    def gerar(self, empresa_id: int) -> list[str]:
        linhas_inm = []

        # 1. Pegar todos os cod_part distintos no C100 da empresa
        query_cod_part = text("""
            SELECT DISTINCT c100.cod_part
            FROM registro_c100 c100
            WHERE c100.empresa_id = :empresa_id
              AND c100.cod_part IS NOT NULL
        """)
        participantes = [
            row.cod_part
            for row in self.session.execute(query_cod_part, {"empresa_id": empresa_id}).mappings().all()
        ]

        for cod_part in participantes:
            # 2. Buscar a UF do participante (0150) dentro da mesma empresa
            query_uf = text("""
                SELECT uf
                FROM registro_0150
                WHERE cod_part = :cod_part
                  AND empresa_id = :empresa_id
            """)
            uf = self.session.execute(query_uf, {"cod_part": cod_part, "empresa_id": empresa_id}).scalar()
            if not uf:
                continue  # se não encontrou a UF, pula

            # 3. Buscar todos os C100 IDs desse participante
            query_c100 = text("""
                SELECT id
                FROM registro_c100
                WHERE cod_part = :cod_part
                  AND empresa_id = :empresa_id
            """)
            c100_ids = [
                row.id
                for row in self.session.execute(query_c100, {"cod_part": cod_part, "empresa_id": empresa_id}).mappings().all()
            ]
            if not c100_ids:
                continue

            # 4. Buscar todos os C190 desses C100
            query_c190 = text("""
                SELECT 
                    cst_icms, 
                    cfop, 
                    aliq_icms, 
                    vl_opr, 
                    vl_bc_icms, 
                    vl_icms, 
                    vl_ipi
                FROM registro_c190
                WHERE c100_id IN :c100_ids
                  AND empresa_id = :empresa_id
            """)
            registros_c190 = self.session.execute(
                query_c190, {"c100_ids": tuple(c100_ids), "empresa_id": empresa_id}
            ).mappings().all()

            # 5. Montar os INM
            for reg in registros_c190:
                linhas_inm.append(builderINM(reg, uf))

        return linhas_inm
