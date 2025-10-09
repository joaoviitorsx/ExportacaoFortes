from sqlalchemy import text
from typing import Dict, Any, List
from .builderNFM import builderNFM

class ExportarNFM:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

    def getNFM(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT
                c.ind_oper, c.ind_emit, c.cod_part, c.cod_mod, c.cod_sit, c.ser,
                c.num_doc, c.chv_nfe, c.dt_doc, c.dt_e_s, c.vl_doc, c.ind_pgto,
                c.vl_desc, c.vl_merc, c.ind_frt, c.vl_frt, c.vl_seg, c.vl_out_da,
                c.vl_bc_icms, c.vl_icms, c.vl_bc_icms_st, c.vl_icms_st, c.vl_ipi,
                c.vl_pis, c.vl_cofins,
                (SELECT filial 
                FROM registro_0000 
                WHERE empresa_id = c.empresa_id 
                AND ativo = 1 
                LIMIT 1) AS estabelecimento,
                (SELECT COUNT(1) 
                FROM registro_c170 
                WHERE c100_id = c.id 
                AND ativo = 1) AS qtd_itens
            FROM registro_c100 c
            WHERE
                c.empresa_id = :empresa_id
                AND c.ativo = 1
                AND c.cod_mod IN ('01', '1B', '04', '55')
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
            linha_formatada = builderNFM(dados_doc)
            linhas_nfm.append(linha_formatada)

        return linhas_nfm