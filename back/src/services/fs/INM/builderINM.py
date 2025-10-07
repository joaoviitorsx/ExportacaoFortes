from typing import Dict, Any
from ....utils.fsFormat import formatarValor

def builderINM(dados: Dict[str, Any]) -> str:
    campos = [''] * 34

    valor_operacao = dados.get("vl_opr") or 0.0
    uf = dados.get("uf") or ""
    cfop = dados.get("cfop") or ""
    base_icms = dados.get("vl_bc_icms") or 0.0
    aliq_icms = dados.get("aliq_icms") or 0.0
    valor_icms = dados.get("vl_icms") or 0.0
    valor_ipi = dados.get("vl_ipi") or 0.0
    
    valor_icms_st = dados.get("vl_icms_st") or 0.0
    
    empresa_simples = dados.get("empresa_simples", False)
    
    cst_icms = str(dados.get("cst_icms") or "").zfill(3)
    csta = ""
    cstb = ""
    csosn_cod = ""
    csosn = ""

    if empresa_simples:
        csosn_cod = cst_icms[0] if cst_icms else ""
        csosn = cst_icms[1:] if len(cst_icms) > 1 else ""
    else:
        csta = cst_icms[0] if cst_icms else ""
        cstb = cst_icms[1:] if len(cst_icms) > 1 else ""

    # Lógica para Isentas e Outras de ICMS
    isentas_icms = valor_operacao if cstb in ["40", "41", "50", "60"] else 0.0
    outras_icms = valor_operacao if cstb in ["90"] else 0.0

    substituicao_icms = "S" if valor_icms_st > 0 else "N"
    substituicao_ipi = "S" if valor_ipi > 0 else "N" 
    
    campos[0] = "INM"                                    # 01 - Tipo de Registro
    campos[1] = formatarValor(valor_operacao)            # 02 - Valor
    campos[2] = uf                                       # 03 - UF
    campos[3] = cfop                                     # 04 - CFOP
    campos[4] = ""                                       # 05 - CFOP Transferencia (vazio por padrão)
    campos[5] = formatarValor(base_icms)                 # 06 - Base de Calculo ICMS
    campos[6] = formatarValor(aliq_icms)                 # 07 - Alíquota do ICMS
    campos[7] = formatarValor(valor_icms)                # 08 - Valor do ICMS
    campos[8] = formatarValor(isentas_icms)              # 09 - Isentas do ICMS
    campos[9] = formatarValor(outras_icms)               # 10 - Outras do ICMS
    campos[10] = ""                                      # 11 - Base de Calculo do IPI (não disponível no C190)
    campos[11] = formatarValor(valor_ipi)                # 12 - Valor do IPI
    campos[12] = ""                                      # 13 - Isentas do IPI (lógica complexa, padrão 0)
    campos[13] = ""                                      # 14 - Outras do IPI (lógica complexa, padrão 0)
    campos[14] = substituicao_icms                       # 15 - Substituição ICMS 
    campos[15] = substituicao_ipi                        # 16 - Substituição IPI
    campos[16] = "N"                                     # 17 - Substituição COFINS (padrão 'N')
    campos[17] = "N"                                     # 18 - Substituição PIS/PASEP (padrão 'N')
    campos[18] = csta                                    # 19 - CSTA
    campos[19] = cstb                                    # 20 - CSTB
    campos[20] = csosn_cod                               # 21 - Codigo da Situação Tributaria do CSOSN
    campos[21] = csosn                                   # 22 - CSOSN
    campos[22] = ""                                      # 23 - CST IPI (não disponível no C190)
    campos[23] = "N"                                     # 24 - COFINS Monofasico (padrão 'N')
    campos[24] = "N"                                     # 25 - PIS Monofasico (padrão 'N')
    campos[25] = "N"                                     # 26 - Calcula Fecop (padrão 'N')
    campos[26] = ""                                      # 27 - Aliq. Subst. (Decreto)
    campos[27] = ""                                      # 28 - Base de Calculo do FCP - Normal
    campos[28] = ""                                      # 29 - Aliquota do FCP - Normal
    campos[29] = ""                                      # 30 - Valor do FCP - Normal
    campos[30] = ""                                      # 31 - Base de Calculo do FCP - Subst. Trib.
    campos[31] = ""                                      # 32 - Alíquota do FCP - Subst. Trib.
    campos[32] = ""                                      # 33 - Valor do FCP - Subst. Trib.
    campos[33] = ""                                      # 34 - Aliquota do ICMS Deferido

    return "|".join(map(str, campos)) + "|"