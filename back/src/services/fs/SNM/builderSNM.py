from typing import Dict, Any
from ....utils.fsFormat import formatarValor

def builderSNM(dados: Dict[str, Any]) -> str:
    vl_item = float(dados.get("vl_item", 0) or 0)
    vl_desc = float(dados.get("vl_desc", 0) or 0)
    frete_rateado = float(dados.get("frete_rateado", 0) or 0)
    seguro_rateado = float(dados.get("seguro_rateado", 0) or 0)
    outras_desp_rateado = float(dados.get("outras_desp_rateado", 0) or 0)
    
    custo_aquisicao = vl_item + frete_rateado + seguro_rateado + outras_desp_rateado - vl_desc
    
    # Normalizar fornecedor_simples
    fornecedor_simples_raw = str(dados.get("fornecedor_simples", "")).strip()
    fornecedorSimples = fornecedor_simples_raw == "True"
    
    # Pegar alíquota do cadastro
    aliquota_cadastro = str(dados.get("aliquota_cadastro", "")).strip().upper()
    
    # Calcular alíquota final (mesma lógica do PNM)
    aliquota_final = 0
    if aliquota_cadastro and aliquota_cadastro not in ["", "None", "null", "ST", "ISENTO"]:
        try:
            aliquota = float(aliquota_cadastro.replace('%', '').replace(',', '.'))
            if fornecedorSimples:
                # Fornecedor Simples: alíquota + 3%
                aliquota_final = aliquota + 3.0
            else:
                # Fornecedor Normal: alíquota sem adicional
                aliquota_final = aliquota
        except (ValueError, AttributeError):
            aliquota_final = float(dados.get("aliq_icms", 0) or 0)
    else:
        aliquota_final = float(dados.get("aliq_icms", 0) or 0)
    
    # Validação
    if custo_aquisicao < 0:
        print(f"[AVISO SNM] Custo negativo ajustado para 0")
        custo_aquisicao = 0

    campos = [
        "SNM",                                        # Campo 1: Tipo de Registro
        "1",                                          # Campo 2: Tipo (1=Agregação)
        formatarValor(custo_aquisicao),               # Campo 3: Custo da Aquisição
        "",                                           # Campo 4: Agregação (%) - vazio para tipo 1
        formatarValor(custo_aquisicao),               # Campo 5: Base de Cálculo
        formatarValor(aliquota_final),                # Campo 6: Alíquota (com ou sem +3%)
        "",                                           # Campo 7: Crédito de Origem
        "",                                           # Campo 8: Já Recolhido
        "N"                                           # Campo 9: Calcula Fecop
    ]

    return "|".join(campos)