from sqlalchemy import text
from typing import Dict, Any, List
from .builderNFM import builderNFM

class ExportarNFM:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

    def cabecalhos(self) -> List[Dict[str, Any]]:
        query = text(
            """
            SELECT
                ind_oper, cod_mod, cod_part, ser, num_doc, cod_sit, chv_nfe,
                dt_doc, dt_e_s, vl_doc, vl_desc, vl_merc, vl_frt, vl_seg,
                vl_out_da, vl_bc_icms, vl_icms, vl_bc_icms_st, vl_icms_st,
                vl_ipi, vl_pis, vl_cofins, ind_frt
            FROM registro_c100
            WHERE
                empresa_id = :empresa_id
                AND cod_mod IN ('01', '1B', '04', '55')
            ORDER BY dt_doc, num_doc;
            """
        )
        
        result = self.session.execute(query, {"empresa_id": self.empresa_id})
        return list(result.mappings().all())

    def gerar(self) -> List[str]:
        cabecalhos = self.cabecalhos()
        if not cabecalhos:
            return []

        linhas_nfm: List[str] = []
        for dados_cabecalho in cabecalhos:
            linha_formatada = builderNFM(dados_cabecalho)
            linhas_nfm.append(linha_formatada)

        return linhas_nfm