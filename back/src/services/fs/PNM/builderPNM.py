from typing import Dict, Any
from src.utils.fsFormat import formatarValor, tributacaoICMS

def builderPNM(dados: Dict[str, Any]) -> str:
    campos = [''] * 121
    cst_icms = str(dados.get("cst_icms") or "").zfill(3)
    csta = cst_icms[0]
    cstb = cst_icms[1:]

    campos[0] = "PNM"                                              # 1 - Tipo
    campos[1] = str(dados.get("cod_item", ''))                     # 2 - Produto
    campos[2] = str(dados.get("cfop", ''))                         # 3 - CFOP
    campos[4] = csta                                               # 5 - CSTA
    campos[5] = cstb                                               # 6 - CSTB
    campos[6] = str(dados.get("unid", ''))                         # 7 - Unidade
    campos[7] = formatarValor(dados.get("qtd"), 4)                 # 8 - Quantidade
    campos[8] = formatarValor(dados.get("vl_item"))                # 9 - Valor bruto
    campos[9] = formatarValor(dados.get("vl_desc"))                # 10 - Valor Desconto
    
    campos[10] = tributacaoICMS(cstb)                    # 11 - Trib. ICMS
    campos[11] = formatarValor(dados.get("vl_bc_icms"))            # 12 - Base ICMS
    campos[12] = formatarValor(dados.get("aliq_icms"))             # 13 - Aliq. ICMS
    campos[13] = formatarValor(dados.get("vl_bc_icms_st"))         # 14 - Base ST
    campos[15] = formatarValor(dados.get("aliq_st"))               # 16 - Aliq. ST
    campos[19] = formatarValor(dados.get("vl_icms_st"))            # 20 - Valor ST
    campos[21] = formatarValor(dados.get("vl_icms"))               # 22 - Valor ICMS

    campos[32] = formatarValor(dados.get("vl_bc_ipi"))             # 33 - Base IPI
    campos[33] = formatarValor(dados.get("aliq_ipi"))              # 34 - Aliq. IPI
    campos[34] = formatarValor(dados.get("vl_ipi"))                # 35 - Valor IPI
    campos[35] = str(dados.get("cst_ipi", ''))                     # 36 - CST IPI

    campos[36] = str(dados.get("cst_cofins", ''))                  # 37 - CST COFINS
    campos[37] = str(dados.get("cst_pis", ''))                     # 38 - CST PIS
    campos[38] = formatarValor(dados.get("vl_bc_cofins"))          # 39 - Base COFINS
    campos[39] = formatarValor(dados.get("vl_bc_pis"))             # 40 - Base PIS
    campos[40] = formatarValor(dados.get("frete_rateado"))         # 41 - Frete
    campos[41] = formatarValor(dados.get("seguro_rateado"))        # 42 - Seguro
    
    valor_total = (
        float(dados.get("vl_item", 0) or 0) +
        float(dados.get("frete_rateado", 0) or 0) +
        float(dados.get("seguro_rateado", 0) or 0) +
        float(dados.get("outras_desp_rateado", 0) or 0) -
        float(dados.get("vl_desc", 0) or 0)
    )
    campos[43] = formatarValor(valor_total)                        # 44 - Valor total

    campos[50] = "2" if float(dados.get("aliq_cofins_reais") or 0) > 0 else "1" # 51 - Tipo calc. COFINS
    campos[51] = formatarValor(dados.get("aliq_cofins"))           # 52 - Aliq. COFINS %
    campos[52] = formatarValor(dados.get("aliq_cofins_reais"), 4)   # 53 - Aliq. COFINS R$
    campos[53] = formatarValor(dados.get("vl_cofins"))             # 54 - Valor COFINS

    campos[54] = "2" if float(dados.get("aliq_pis_reais") or 0) > 0 else "1" # 55 - Tipo calc. PIS
    campos[55] = formatarValor(dados.get("aliq_pis"))              # 56 - Aliq. PIS %
    campos[56] = formatarValor(dados.get("aliq_pis_reais"), 4)      # 57 - Aliq. PIS R$
    campos[57] = formatarValor(dados.get("vl_pis"))                # 58 - Valor PIS
    
    campos[58] = str(dados.get("cod_cta", ''))                     # 59 - Cod. ajuste (pode precisar de outra fonte)
    campos[61] = formatarValor(dados.get("outras_desp_rateado"))   # 62 - Outras despesas
    campos[62] = str(dados.get("cod_cta", ''))                     # 63 - Cod. contábil
    campos[64] = str(dados.get("cod_ncm", ''))                     # 65 - NCM
    campos[114] = str(dados.get("cod_cest", ''))                   # 115 - CEST

    return "|".join(campos)