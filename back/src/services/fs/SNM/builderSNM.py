from typing import Dict, Any

from src.utils.fsFormat import formatarValor

def builderSNM(dados: Dict[str, Any]) -> str:
    campos = [''] * 14

    cst_icms = str(dados.get("cst_icms") or "000").zfill(3)
    csta = cst_icms[0]
    cstb = cst_icms[1:]

    vl_opr = dados.get("vl_opr", 0.0)
    valor_isentas = 0.0
    valor_outras = 0.0

    # Lógica condicional para os campos "Valor de Isentas" e "Valor de Outras"
    if cstb in ('40', '41', '50'):
        valor_isentas = vl_opr
    elif cstb in ('90',): # Adicione outros CSTs se necessário
        valor_outras = vl_opr
    
    campos[0] = "SNM"                                           # 1 - Tipo
    campos[1] = str(dados.get("num_doc", ''))                   # 2 - Código do Documento
    campos[2] = str(dados.get("cfop", ''))                      # 3 - CFOP
    campos[3] = csta                                            # 4 - CSTA
    campos[4] = cstb                                            # 5 - CSTB
    campos[5] = formatarValor(dados.get("aliq_icms"))           # 6 - Alíquota do ICMS
    
    campos[6] = formatarValor(vl_opr)                           # 7 - Valor Contábil
    campos[7] = formatarValor(dados.get("vl_bc_icms"))          # 8 - Base de Cálculo do ICMS
    campos[8] = formatarValor(dados.get("vl_icms"))             # 9 - Valor do ICMS
    campos[9] = formatarValor(valor_isentas)                    # 10 - Valor de Isentas
    campos[10] = formatarValor(valor_outras)                    # 11 - Valor de Outras
    campos[11] = formatarValor(dados.get("vl_bc_icms_st"))      # 12 - Base de Cálculo do ICMS ST
    campos[12] = formatarValor(dados.get("vl_icms_st"))         # 13 - Valor do ICMS ST
    campos[13] = formatarValor(dados.get("vl_ipi"))             # 14 - Valor do IPI

    return "|".join(campos)