from src.utils.fsFormat import digitos, validacaoText


def builderPNM(dados: dict) -> str:
    """
    Monta a linha PNM (Produtos da Nota Fiscal de Mercadorias)
    conforme layout Fortes Fiscal (83 campos).
    """

    tipo = "PNM"

    # Quebra do CST ICMS
    cst_icms = str(dados.get("cst_icms") or "").zfill(3)
    csta = cst_icms[0] if cst_icms else ""
    cstb = cst_icms[1:] if len(cst_icms) == 3 else ""

    # Tributação ICMS (campo 11)
    vl_icms = float(dados.get("vl_icms") or 0)
    if vl_icms > 0:
        tributacao_icms = "1"
    elif cstb in ("40", "41", "50"):
        tributacao_icms = "2"
    elif cstb in ("60", "90"):
        tributacao_icms = "3"
    else:
        tributacao_icms = ""

    # Valor total (campo 44)
    vl_item = float(dados.get("vl_item") or 0)
    vl_frete = float(dados.get("frete_rateado") or 0)
    vl_seg = float(dados.get("seguro_rateado") or 0)
    vl_outras = float(dados.get("outras_desp_rateado") or 0)
    vl_desc = float(dados.get("vl_desc") or 0)
    valor_total = vl_item + vl_frete + vl_seg + vl_outras - vl_desc

    # Campos já tratados
    campos = [
        tipo,                                      # 1 - Tipo registro
        validacaoText(dados.get("cod_item"), 9),   # 2 - Produto
        digitos(dados.get("cfop")),                # 3 - CFOP
        "",                                        # 4 - CFOP transf.
        csta,                                      # 5 - CSTA
        cstb,                                      # 6 - CSTB
        validacaoText(dados.get("unid"), 6),       # 7 - Unidade
        validacaoText(dados.get("qtd"), 9),        # 8 - Quantidade
        validacaoText(dados.get("vl_item"), 15),   # 9 - Valor bruto
        validacaoText(dados.get("vl_ipi"), 15),    # 10 - Valor IPI
        tributacao_icms,                           # 11 - Trib. ICMS
        validacaoText(dados.get("vl_bc_icms"), 15),# 12 - Base ICMS
        validacaoText(dados.get("aliq_icms"), 5),  # 13 - Aliq. ICMS
        validacaoText(dados.get("vl_bc_icms_st"), 15), # 14 - Base ST
        validacaoText(dados.get("vl_icms_st"), 15),    # 15 - Valor ST
    ]

    # 16–31 Reservados
    campos.extend([""] * (32 - len(campos)))

    campos.extend([
        "",                                        # 32 - Tipo trib. IPI
        validacaoText(dados.get("vl_bc_ipi"), 15), # 33 - Base IPI
        validacaoText(dados.get("aliq_ipi"), 5),   # 34 - Aliq. IPI
        validacaoText(dados.get("vl_ipi"), 15),    # 35 - Valor IPI
        digitos(dados.get("cst_ipi")),             # 36 - CST IPI
        digitos(dados.get("cst_cofins")),          # 37 - CST COFINS
        digitos(dados.get("cst_pis")),             # 38 - CST PIS
        validacaoText(dados.get("vl_bc_cofins"), 15), # 39 - Base COFINS
        validacaoText(dados.get("vl_bc_pis"), 15),    # 40 - Base PIS
        validacaoText(dados.get("frete_rateado"), 15),# 41 - Frete rateado
        validacaoText(dados.get("seguro_rateado"), 15),# 42 - Seguro rateado
        validacaoText(dados.get("vl_desc"), 15),   # 43 - Desconto
        f"{valor_total:.2f}",                      # 44 - Valor total
        "",                                        # 45 - Nat. receita COFINS
        "",                                        # 46 - Nat. receita PIS
        "",                                        # 47 - Reservado
        "",                                        # 48 - Reservado
        "",                                        # 49 - CSOSN origem
        "",                                        # 50 - CSOSN código
        "2" if float(dados.get("aliq_cofins_reais") or 0) > 0 else "1", # 51 - Tipo calc. COFINS
        validacaoText(dados.get("aliq_cofins"), 7),      # 52 - Aliq. COFINS %
        validacaoText(dados.get("aliq_cofins_reais"), 5),# 53 - Aliq. COFINS R$
        validacaoText(dados.get("vl_cofins"), 15),       # 54 - Valor COFINS
        "2" if float(dados.get("aliq_pis_reais") or 0) > 0 else "1", # 55 - Tipo calc. PIS
        validacaoText(dados.get("aliq_pis"), 7),         # 56 - Aliq. PIS %
        validacaoText(dados.get("aliq_pis_reais"), 5),   # 57 - Aliq. PIS R$
        validacaoText(dados.get("vl_pis"), 15),          # 58 - Valor PIS
        "",                                        # 59 - Cod. ajuste fiscal
        "",                                        # 60 - Reservado
        "",                                        # 61 - Reservado
        validacaoText(dados.get("outras_desp_rateado"), 15), # 62 - Outras despesas
        validacaoText(dados.get("cod_cta"), 15),   # 63 - Cod. contábil
    ])

    # 64–82 Reservados
    campos.extend([""] * (83 - len(campos)))

    campos.append(validacaoText(dados.get("vl_icms"), 15))  # 83 - Exclusão BC PIS/COFINS

    return "|".join(map(str, campos))
