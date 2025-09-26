from typing import Dict, Any
from src.utils.fsFormat import formatarValor, tributacaoICMS 

def builderPNM(dados: Dict[str, Any]) -> str:
    campos = [''] * 121
    cst_icms = str(dados.get("cst_icms") or "").zfill(3)
    csta = cst_icms[0]
    cstb = cst_icms[1:]

    aliquota_final = dados.get("aliquota_cadastro")
    
    campos[0] = "PNM"
    campos[1] = str(dados.get("cod_item", ''))
    campos[2] = str(dados.get("cfop", ''))
    campos[4] = csta
    campos[5] = cstb
    campos[6] = str(dados.get("unid", ''))
    campos[7] = formatarValor(dados.get("qtd"), 4)
    campos[8] = formatarValor(dados.get("vl_item"))
    campos[9] = formatarValor(dados.get("vl_desc"))
    
    campos[10] = tributacaoICMS(cstb, aliquota_final)
    
    campos[11] = formatarValor(dados.get("vl_bc_icms"))
    campos[12] = formatarValor(aliquota_final)
    campos[13] = formatarValor(dados.get("vl_bc_icms_st"))
    campos[15] = formatarValor(dados.get("aliq_st"))
    campos[19] = formatarValor(dados.get("vl_icms_st"))
    campos[21] = formatarValor(dados.get("vl_icms"))
    campos[32] = formatarValor(dados.get("vl_bc_ipi"))
    campos[33] = formatarValor(dados.get("aliq_ipi"))
    campos[34] = formatarValor(dados.get("vl_ipi"))
    campos[35] = str(dados.get("cst_ipi", ''))
    campos[36] = str(dados.get("cst_cofins", ''))
    campos[37] = str(dados.get("cst_pis", ''))
    campos[38] = formatarValor(dados.get("vl_bc_cofins"))
    campos[39] = formatarValor(dados.get("vl_bc_pis"))
    campos[40] = formatarValor(dados.get("frete_rateado"))
    campos[41] = formatarValor(dados.get("seguro_rateado"))
    
    valor_total = (
        float(dados.get("vl_item", 0) or 0) +
        float(dados.get("frete_rateado", 0) or 0) +
        float(dados.get("seguro_rateado", 0) or 0) +
        float(dados.get("outras_desp_rateado", 0) or 0) -
        float(dados.get("vl_desc", 0) or 0)
    )
    campos[43] = formatarValor(valor_total)

    campos[50] = "2" if float(dados.get("aliq_cofins_reais") or 0) > 0 else "1"
    campos[51] = formatarValor(dados.get("aliq_cofins"))
    campos[52] = formatarValor(dados.get("aliq_cofins_reais"), 4)
    campos[53] = formatarValor(dados.get("vl_cofins"))
    campos[54] = "2" if float(dados.get("aliq_pis_reais") or 0) > 0 else "1"
    campos[55] = formatarValor(dados.get("aliq_pis"))
    campos[56] = formatarValor(dados.get("aliq_pis_reais"), 4)
    campos[57] = formatarValor(dados.get("vl_pis"))
    
    campos[58] = str(dados.get("cod_cta", ''))
    campos[61] = formatarValor(dados.get("outras_desp_rateado"))
    campos[62] = str(dados.get("cod_cta", ''))
    campos[64] = str(dados.get("cod_ncm", ''))
    campos[114] = str(dados.get("cod_cest", ''))

    return "|".join(campos)