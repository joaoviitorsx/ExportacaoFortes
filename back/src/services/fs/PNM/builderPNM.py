# Arquivo: src/services/fs/PNM/builderPNM.py

from typing import Dict, Any

def _format_value(value: Any, precision: int = 2) -> str:
    """Formata um valor para string, tratando None e aplicando precisão numérica."""
    if value is None or value == '':
        return ''
    try:
        # Tenta converter para float e formatar
        return f'{float(value):.{precision}f}'.replace(',', '.')
    except (ValueError, TypeError):
        # Se falhar, retorna como string
        return str(value)

def _definir_tributacao_icms(cstb: str) -> str:
    """Define o código de Tributação ICMS (Campo 11 do PNM) com base no CSTB."""
    if not cstb:
        return '1'
    if cstb in ('10', '30', '60', '70', '90'):
        return '3'  # Substituição Tributária
    if cstb == '20':
        return '2'  # Redução na Base de Cálculo
    if cstb in ('40', '41', '50'):
        return '4'  # Isenta
    if cstb == '51':
        return '5'  # Diferimento
    return '1'  # Tributado Integralmente (Default para 00, etc.)

def builderPNM(dados: Dict[str, Any]) -> str:
    """
    Monta a linha PNM (121 campos) a partir de um dicionário de dados enriquecidos.
    """
    campos = [''] * 121

    # --- Tratamento de dados de entrada ---
    cst_icms = str(dados.get("cst_icms") or "").zfill(3)
    csta = cst_icms[0]
    cstb = cst_icms[1:]

    # --- Preenchimento dos campos por índice (inicia em 0) ---
    campos[0] = "PNM"                                              # 1 - Tipo
    campos[1] = str(dados.get("cod_item", ''))                     # 2 - Produto
    campos[2] = str(dados.get("cfop", ''))                         # 3 - CFOP
    campos[4] = csta                                               # 5 - CSTA
    campos[5] = cstb                                               # 6 - CSTB
    campos[6] = str(dados.get("unid", ''))                         # 7 - Unidade
    campos[7] = _format_value(dados.get("qtd"), 4)                 # 8 - Quantidade
    campos[8] = _format_value(dados.get("vl_item"))                # 9 - Valor bruto
    campos[9] = _format_value(dados.get("vl_desc"))                # 10 - Valor Desconto
    
    campos[10] = _definir_tributacao_icms(cstb)                    # 11 - Trib. ICMS
    campos[11] = _format_value(dados.get("vl_bc_icms"))            # 12 - Base ICMS
    campos[12] = _format_value(dados.get("aliq_icms"))             # 13 - Aliq. ICMS
    campos[13] = _format_value(dados.get("vl_bc_icms_st"))         # 14 - Base ST
    campos[15] = _format_value(dados.get("aliq_st"))               # 16 - Aliq. ST
    campos[19] = _format_value(dados.get("vl_icms_st"))            # 20 - Valor ST
    campos[21] = _format_value(dados.get("vl_icms"))               # 22 - Valor ICMS

    campos[32] = _format_value(dados.get("vl_bc_ipi"))             # 33 - Base IPI
    campos[33] = _format_value(dados.get("aliq_ipi"))              # 34 - Aliq. IPI
    campos[34] = _format_value(dados.get("vl_ipi"))                # 35 - Valor IPI
    campos[35] = str(dados.get("cst_ipi", ''))                     # 36 - CST IPI

    campos[36] = str(dados.get("cst_cofins", ''))                  # 37 - CST COFINS
    campos[37] = str(dados.get("cst_pis", ''))                     # 38 - CST PIS
    campos[38] = _format_value(dados.get("vl_bc_cofins"))          # 39 - Base COFINS
    campos[39] = _format_value(dados.get("vl_bc_pis"))             # 40 - Base PIS
    campos[40] = _format_value(dados.get("frete_rateado"))         # 41 - Frete
    campos[41] = _format_value(dados.get("seguro_rateado"))        # 42 - Seguro
    
    valor_total = (
        float(dados.get("vl_item", 0) or 0) +
        float(dados.get("frete_rateado", 0) or 0) +
        float(dados.get("seguro_rateado", 0) or 0) +
        float(dados.get("outras_desp_rateado", 0) or 0) -
        float(dados.get("vl_desc", 0) or 0)
    )
    campos[43] = _format_value(valor_total)                        # 44 - Valor total

    campos[50] = "2" if float(dados.get("aliq_cofins_reais") or 0) > 0 else "1" # 51 - Tipo calc. COFINS
    campos[51] = _format_value(dados.get("aliq_cofins"))           # 52 - Aliq. COFINS %
    campos[52] = _format_value(dados.get("aliq_cofins_reais"), 4)   # 53 - Aliq. COFINS R$
    campos[53] = _format_value(dados.get("vl_cofins"))             # 54 - Valor COFINS

    campos[54] = "2" if float(dados.get("aliq_pis_reais") or 0) > 0 else "1" # 55 - Tipo calc. PIS
    campos[55] = _format_value(dados.get("aliq_pis"))              # 56 - Aliq. PIS %
    campos[56] = _format_value(dados.get("aliq_pis_reais"), 4)      # 57 - Aliq. PIS R$
    campos[57] = _format_value(dados.get("vl_pis"))                # 58 - Valor PIS
    
    campos[58] = str(dados.get("cod_cta", ''))                     # 59 - Cod. ajuste (pode precisar de outra fonte)
    campos[61] = _format_value(dados.get("outras_desp_rateado"))   # 62 - Outras despesas
    campos[62] = str(dados.get("cod_cta", ''))                     # 63 - Cod. contábil
    campos[64] = str(dados.get("cod_ncm", ''))                     # 65 - NCM
    campos[114] = str(dados.get("cod_cest", ''))                   # 115 - CEST

    return "|".join(campos)