from typing import Dict, Any
from ....utils.fsFormat import digitos, validacaoText

def builderPRO(produto_data: Dict[str, Any]) -> str:

    cod_item = validacaoText(produto_data.get("cod_item", ""), 9)
    descr_item = validacaoText(produto_data.get("descr_item", ""), 60).upper()
    cod_barra = validacaoText(produto_data.get("cod_barra", ""), 20)
    unid_inv = validacaoText(produto_data.get("unid_inv", ""), 6)
    cod_ncm = validacaoText(produto_data.get("cod_ncm", ""), 20)
    cod_gen = validacaoText(produto_data.get("cod_gen", ""), 2)
    cest = validacaoText(produto_data.get("cest", ""), 7)

    cod_barra = digitos(produto_data.get("cod_barra", ""))
    
    desativado_flag = "N" if produto_data.get("ativo", True) else "S"

    campos = [''] * 55

    campos[0] = "PRO"                               # 1. Tipo de Registro
    campos[1] = cod_item[:9]                        # 2. Código
    campos[2] = descr_item[:60]                     # 3. Descrição
    campos[3] = cod_item[:60]                       # 4. Código Utilizado Estab.
    campos[4] = cod_ncm[:20]                        # 5. Código NCM
    campos[5] = unid_inv[:6]                        # 6. Unidade de Medida Padrão
    campos[6] = ""                                  # 7. Unidade Medida DIEF
    campos[7] = ""                                  # 8. Unidade Medida CENFOP
    campos[8] = ""                                  # 9. Classificação
    campos[9] = "1"                                  # 10. Grupo
    campos[10] = cod_gen[:2]                        # 11. Gênero
    campos[11] = cod_barra[:20]                     # 12. Código de Barras
    campos[12] = ""                                 # 13. Redução
    campos[13] = ""                                 # 14. Código GAM57
    campos[14] = ""                                 # 15. CST ICMS
    campos[15] = ""                                 # 16. CST IPI
    campos[16] = ""                                 # 17. CST COFINS
    campos[17] = ""                                 # 18. CST PIS
    campos[18] = ""                                 # 19. Código ANP
    campos[19] = ""                                 # 20. CST ICMS (Simples Nacional)
    campos[20] = ""                                 # 21. CSOSN
    campos[21] = ""                                 # 22. Produto Específico
    campos[22] = ""                                 # 23. Tipo de Medicamento
    campos[23] = desativado_flag                    # 24. Desativado
    campos[24] = ""                                 # 25. Código Indicador de Contribuição Previdenciária
    campos[25] = ""                                 # 26. Tipo de Tributação - DIA
    campos[26] = ""                                 # 27. Codificação NVE
    campos[27] = ""                                 # 28. Indicador Especial
    campos[28] = ""                                 # 29. Código da Apuração
    campos[29] = ""                                 # 30. Código TIPI
    campos[30] = ""                                 # 31. Código Combustível DIEF(PA)
    campos[31] = ""                                 # 32. Percentual de Incentivo
    campos[32] = ""                                 # 33. Prazo de Fruição
    campos[33] = ""                                 # 34. Indicador Especial de Incentivo
    campos[34] = ""                                 # 35. Percentual da CSL
    campos[35] = ""                                 # 36. Percentual do IRPJ
    campos[36] = "N"                                # 37. Alíq. ICMS Interna
    campos[37] = ""                                 # 38. Códigos da Receita (Produto Específico)
    campos[38] = ""                                 # 39. Cód. Receita COFINS
    campos[39] = ""                                 # 40. Cód. Receita PIS
    campos[40] = cest[:7]                           # 41. Cód. CEST
    campos[41] = "N"                                 # 42. Custo de Aquisição
    campos[42] = "N"                                # 43. Substituição de ICMS
    campos[43] = "N"                                # 44. Substituição de IPI
    campos[44] = "N"                                # 45. Substituição de COFINS
    campos[45] = "N"                                # 46. Substituição de PIS/PASEP
    campos[46] = "N"                                # 47. Tributação Monofásica de COFINS
    campos[47] = ""                                # 48. Tributação Monofásica de PIS
    campos[48] = ""                                 # 49. Apuração do PIS/COFINS
    campos[49] = ""                                 # 50. Cód. Receita Retido COFINS
    campos[50] = ""                                 # 51. Cód. Receita Retido PIS
    campos[51] = ""                                 # 52. Cód. Receita Retido CSL
    campos[52] = ""                                 # 53. Cód. Receita Retido IRPJ
    campos[53] = ""                                 # 54. Cód. Receita Retido COSIRF
    campos[54] = "N"                                # 55. Decreto 20.686/99 (AM)

    return "|".join(campos) + "|"