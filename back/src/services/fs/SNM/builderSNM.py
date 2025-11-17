from typing import Dict, Any
from ....utils.fsFormat import formatarValor

def builderSNM(dados: Dict[str, Any]) -> str:
    custo_aquisicao = dados.get("vl_opr")

    campos = [
        "SNM",                                        # Campo 1: Tipo de Registro
        "1",                                          # Campo 2: Tipo (Agregação)
        formatarValor(custo_aquisicao),               # Campo 3: Custo da Aquisição (vl_opr como aproximação)
        "",                                           # Campo 4: Agregação (%) - Não disponível
        formatarValor(custo_aquisicao),               # Campo 5: Base de Cálculo (vl_item - vl_desc * aliquota)
        formatarValor(dados.get("aliq_icms")),        # Campo 6: Alíquota do produto na tabela produtos
        "",                                           # Campo 7: Crédito de Origem - Não disponível
        "",                                           # Campo 8: Já Recolhido - Não disponível
        "N"                                           # Campo 9: Calcula Fecop
    ]

    return "|".join(campos)