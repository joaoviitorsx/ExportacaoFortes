from sqlalchemy import text
from typing import Dict, Any, List
from .builderNFM import builderNFM
from ..PNM.exportarPNM import ExportarPNM
from ..INM.exportarINM import ExportarINM
from ..SNM.exportarSNM import ExportarSNM


class ExportarNFM:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

        self.exportar_pnm = ExportarPNM(session, empresa_id)
        self.exportar_inm = ExportarINM(session, empresa_id)
        self.exportar_snm = ExportarSNM(session, empresa_id)

    def getNFM(self) -> List[Dict[str, Any]]:
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
            JOIN registro_c190 AS c190
                ON c190.c100_id = c.id 
                AND c190.ativo = 1
            WHERE
                c.empresa_id = :empresa_id
                AND c.ativo = 1
                AND c.cod_mod IN ('01', '1B', '04', '55')
            GROUP BY
                c.id, c.ind_oper, c.ind_emit, c.cod_part, c.cod_mod, c.cod_sit, c.ser,
                c.num_doc, c.chv_nfe, c.dt_doc, c.dt_e_s, c.vl_doc, c.ind_pgto,
                c.vl_desc, c.vl_merc, c.ind_frt, c.vl_frt, c.vl_seg, c.vl_out_da,
                c.vl_bc_icms, c.vl_icms, c.vl_bc_icms_st, c.vl_icms_st, c.vl_ipi,
                c.vl_pis, c.vl_cofins, r0.filial
            ORDER BY c.dt_doc, c.num_doc
        """)

        result = self.session.execute(query, {"empresa_id": self.empresa_id})
        return list(result.mappings().all())

    def gerar(self) -> List[str]:
        documentos = self.getNFM()
        if not documentos:
            return []

        linhas_nfm: List[str] = []

        for dados_doc in documentos:
            c100_id = dados_doc["c100_id"]

            linha_nfm = builderNFM(dados_doc)
            linhas_nfm.append(linha_nfm)

            linhas_pnm = self.exportar_pnm.gerar_por_nota(c100_id)
            if linhas_pnm:
                linhas_nfm.extend(linhas_pnm)

            linhas_inm = self.exportar_inm.gerar_por_nota(c100_id)
            if linhas_inm:
                linhas_nfm.extend(linhas_inm)

            linhas_snm = self.exportar_snm.gerar_por_nota(c100_id)
            if linhas_snm:
                linhas_nfm.extend(linhas_snm)

        return linhas_nfm
