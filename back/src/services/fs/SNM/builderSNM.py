from typing import Dict, Any
from ....utils.fsFormat import formatarValor

def builderSNM(dados: Dict[str, Any]) -> str:
    campos = [''] * 10
    custo_aquisicao = dados.get("vl_opr")
    base_calculo_st = dados.get("vl_bc_icms_st")

    campos[0] = "SNM"                                     # Campo 1: Tipo de Registro
    campos[1] = "1"                                       # Campo 2: Tipo (Agregação)
    campos[2] = formatarValor(custo_aquisicao)            # Campo 3: Custo da Aquisição (vl_opr como aproximação)
    campos[3] = ""                                        # Campo 4: Agregação (%) - Não disponível
    campos[4] = formatarValor(custo_aquisicao)            # Campo 5: Base de Cálculo (vl_item - vl_desc * aliquota)
    campos[5] = formatarValor(dados.get("aliq_icms"))     # Campo 6: Alíquota do produto na tabela produtos
    campos[6] = ""                                        # Campo 7: Crédito de Origem - Não disponível
    campos[7] = ""                                        # Campo 8: Já Recolhido - Não disponível
    campos[8] = "N"                                       # Campo 9: Calcula Fecop
    campos[9] = "N"                                       # Campo 10: (Campo extra observado no padrão)

    return "|".join(campos) + "|"