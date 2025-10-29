from typing import Dict, Any
from ....utils.fsFormat import formatarValor, tributacaoICMS 

def builderPNM(dados: Dict[str, Any]) -> str:
    cst_icms = str(dados.get("cst_icms") or "").zfill(3)
    csta = cst_icms[0] if len(cst_icms) == 3 else ''
    cstb = cst_icms[1:] if len(cst_icms) == 3 else ''
    
    is_simples = csta in ['1', '2', '3', '4', '5', '9']
    csosn = cst_icms if is_simples else ''
    
    csta_final = "" if is_simples else csta
    cstb_final = "" if is_simples else cstb

    tipo_calc_cofins = "2" if float(dados.get("aliq_cofins_reais", 0) or 0) > 0 else "1"
    tipo_calc_pis = "2" if float(dados.get("aliq_pis_reais", 0) or 0) > 0 else "1"

    valorTotal = (
        (float(dados.get("vl_item", 0) or 0)) +
        (float(dados.get("frete_rateado", 0) or 0)) +
        (float(dados.get("seguro_rateado", 0) or 0)) +
        (float(dados.get("outras_desp_rateado", 0) or 0)) -
        (float(dados.get("vl_desc", 0) or 0))
    )
    
    cst_confins = str(dados.get("vl_bc_cofins") or "").strip()
    cst_confins_final = cst_confins if cst_confins else formatarValor(dados.get("vl_item"))

    cst_pis = str(dados.get("vl_bc_pis") or "").strip()
    cst_pis_final = cst_pis if cst_pis else formatarValor(dados.get("vl_item"))


    aliquotaProduto = str(dados.get("aliquota_cadastro") or "").strip().upper()
    stOrIsento = aliquotaProduto in ("ST", "ISENTO")

    fornecedorSimples = str(dados.get("fornecedor_simples")).lower() == "true"
    fornecedorDecreto = str(dados.get("fornecedor_decreto")).lower() == "true"
    campo_16 = campo_17 = campo_18 = campo_19 = campo_20 = campo_21 = ""

    if not stOrIsento:
        if fornecedorDecreto:
            pass

        elif fornecedorSimples and not fornecedorDecreto:
            campo_16 = "1"
            campo_17 = "1"
            campo_18 = formatarValor(valorTotal)
            campo_19 = ""
            campo_20 = formatarValor(valorTotal)

            valorAliquota = str(aliquotaProduto).strip()
            if valorAliquota and valorAliquota not in ["", "None", "null"]:
                try:
                    aliquota = float(str(aliquotaProduto).replace('%', '').replace(',', '.'))
                    aliquotaFinal = aliquota + 3.0
                    campo_21 = formatarValor(aliquotaFinal)
                except (ValueError, AttributeError) as e:
                    campo_21 = ""
            else:
                campo_21 = ""   

        elif not fornecedorSimples and not fornecedorDecreto:
            campo_16 = "1"
            campo_17 = "1"
            campo_18 = formatarValor(valorTotal)
            campo_19 = ""
            campo_20 = formatarValor(valorTotal)

            try:
                aliquota = float(str(aliquotaProduto).replace('%', '').replace(',', '.'))
                campo_21 = formatarValor(aliquota)
            except (ValueError, AttributeError) as e:
                campo_21 = ""

    campos = [
        "PNM",                                               # 1. Tipo de registro
        str(dados.get("cod_item", ''))[:9],                  # 2. Produto
        str(dados.get("cfop", ''))[:4],                      # 3. CFOP
        "",                                                  # 4. CFOP Transferencia
        csta_final,                                          # 5. CSTA
        cstb_final,                                          # 6. CSTB
        str(dados.get("unid", ''))[:6],                      # 7. Unidade de Medida
        formatarValor(dados.get("qtd"))[:5],                 # 8. Quantidade
        formatarValor(dados.get("vl_item")),                 # 9. Valor Bruto
        "",                                                  # 10. Valor do IPI (não contribuinte)
        tributacaoICMS(cstb_final, dados.get("aliquota_cadastro")), # 11. Tributação ICMS
        formatarValor(dados.get("vl_bc_icms")),              # 12. Base de Calculo do ICMS
        formatarValor(dados.get("aliq_icms")),               # 13. Aliquota do ICMS
        formatarValor(dados.get("vl_bc_icms_st")),           # 14. Base Calc. Subst. Tributaria
        formatarValor(dados.get("vl_icms_st")),              # 15. ICMS Substituição
        campo_16,                                            # 16. Tipo de Recolhimento
        campo_17,                                            # 17. Tipo de Substituição
        campo_18,                                            # 18. Custo Aquisição Subst. Trib.
        campo_19,                                            # 19. Perc. Agreg. Substituição
        campo_20,                                            # 20. Base de Calc. Subst. Trib (a recolher)
        campo_21,                                            # 21. Aliquota Subst. Tributaria
        "",                                                  # 22. Credito de Origem (ST)
        "N",                                                 # 23. Subst. já Recolhido
        "",                                                  # 24. Custo de Aquisição Antecip.
        "",                                                  # 25. Perc. Agregação Antecipado
        "",                                                  # 26. Aliquota interna (Antec.)
        "",                                                  # 27. Credito de origem (Antec.)
        "",                                                  # 28. Antec. ja recolhido
        "",                                                  # 29. Base de calc. dif. aliquota
        "",                                                  # 30. Aliquota de origem
        "",                                                  # 31. Aliquota interna (Difal)
        "",                                                  # 32. Tipo tributacao IPI
        formatarValor(dados.get("vl_bc_ipi")),               # 33. Base de calc. do IPI
        formatarValor(dados.get("aliq_ipi")),                # 34. Aliquota do IPI
        formatarValor(dados.get("vl_ipi")),                  # 35. Valor do IPI (contribuinte)
        str(dados.get("cst_ipi", '')),                       # 36. CST IPI
        str(dados.get("cst_cofins", '')),                    # 37. CST COFINS
        str(dados.get("cst_pis", '')),                       # 38. CST PIS
        cst_confins_final,                                   # 39. Base de calculo COFINS
        cst_pis_final,                     # 40. Base de calculo PIS
        formatarValor(dados.get("frete_rateado")),           # 41. Valor Frete
        formatarValor(dados.get("seguro_rateado")),          # 42. Valor Seguro
        formatarValor(dados.get("vl_desc")),                 # 43. Valor Desconto
        formatarValor(valorTotal),                           # 44. Valor total
        str(dados.get("cod_nat", ''))[:3],                   # 45. Natureza da receita COFINS
        str(dados.get("cod_nat", ''))[:3],                   # 46. Natureza da receita PIS
        "",                                                  # 47. Indicador Especial (PRODEPE)
        "",                                                  # 48. Codigo da Apuração (PRODEPE)
        csta if is_simples else "",                          # 49. Codigo da situação Tributaria do CSOSN (Origem)
        csosn,                                               # 50. CSOSN
        tipo_calc_cofins,                                    # 51. Tipo de Calculo COFINS
        formatarValor(dados.get("aliq_cofins")),             # 52. Aliquota COFINS (%)
        formatarValor(dados.get("aliq_cofins_reais"), 4),    # 53. Aliquota COFINS (R$)
        formatarValor(dados.get("vl_cofins")),               # 54. Valor COFINS
        tipo_calc_pis,                                       # 55. Tipo de Calculo PIS
        formatarValor(dados.get("aliq_pis")),                # 56. Aliquota PIS (%)
        formatarValor(dados.get("aliq_pis_reais"), 4),       # 57. Aliquota PIS (R$)
        formatarValor(dados.get("vl_pis")),                  # 58. Valor PIS
        "",                                                  # 59. Codigo de Ajuste Fiscal
        "",                                                  # 60. Pedido de Compra
        "",                                                  # 61. Item do pedido de compra
        formatarValor(dados.get("outras_desp_rateado")),     # 62. Outras Despesas
        str(dados.get("cod_cta", ''))[:15],                  # 63. Codigo Contabil
        "0",                                                 # 64. Item Não Compoe Valor Total
        "",                                                  # 65. Natureza da Contribuição do Estorno COFINS
        "",                                                  # 66. Natureza da contribuição do Estorno PIS
        "",                                                  # 67. Natureza do Credito do Estorno COFINS
        "",                                                  # 68. Natureza do Credito do Estorno PIS
        "",                                                  # 69. FCI
        "",                                                  # 70. Item Derivado de Petroleo
        "",                                                  # 71. RECOPI
        "",                                                  # 72. Percentual IPI Devolvido
        "",                                                  # 73. Motivo da Devolução IPI
        "",                                                  # 74. Indicador Especial de Incentivo
        "",                                                  # 75. Valor ICMS Desonerado
        "",                                                  # 76. Motivo da Desoneração do ICMS
        "",                                                  # 77. Base de Calculo - Diferencial de Aliquotas
        "",                                                  # 78. Aliquota FECOP - Diferencial de Aliquotas
        "",                                                  # 79. Aliquota de Origem - Diferencial de Aliquotas
        "",                                                  # 80. Alíquota de Destino - Diferencial de Alíquotas
        "N",                                                 # 81. Calculo Fecop (Decreto 29.560/08)
        "",                                                  # 82. Aliq. Subst. (Decreto 29.560/08)
        formatarValor(dados.get("vl_icms")),                 # 83. Exclusão da BC PIS/COFINS
        "",                                                  # 84. Aliquota de Credito
        "",                                                  # 85. Base de Calculo do FCP Normal
        "",                                                  # 86. Aliquota do FCP - Normal
        "",                                                  # 87. Valor do FCP - Normal
        "",                                                  # 88. Base de Calculo do FCP - Subst. Trib.
        "",                                                  # 89. Aliquota do FCP - Subst. Trib.
        "",                                                  # 90. Valor do FCP - Subst. Trib.
        "N",                                                 # 91. Ressarcimento Substituição Tributaria
        "",                                                  # 92. Especie do Documento Ressarcimento ST
        "",                                                  # 93. Data de Documento Ressarcimento ST
        "",                                                  # 94. Numero do Documento Ressarcimento ST
        "",                                                  # 95. Serie do Documento Ressarcimento ST
        "",                                                  # 96. Chave Eletronica do Documento Ressarcimento ST
        "",                                                  # 97. Codigo do Participante do Documento Ressarcimento ST
        "",                                                  # 98. Codigo do Item do Documento Ressarcimento ST
        "",                                                  # 99. Quantidade do Item do Documento Ressarcimento ST
        "",                                                  # 100. Valor Unitario do Item do Documento Ressarcimento ST
        "",                                                  # 101. Valor Unitario Base Calculo ICMS Pago por Substituição
        "",                                                  # 102. Vr. Unit. BC. ICMS Remetente
        "",                                                  # 103. Aliq. ICMS (%)
        "",                                                  # 104. Vr. Unit. BC. ICMS Retenção
        "",                                                  # 105. Vr. Unit. Credito ICMS
        "",                                                  # 106. Aliq. ICMS ST (%)
        "",                                                  # 107. Vr. Unit. BC. ICMS ST Ressarcimento
        "",                                                  # 108. Codigo Retenção do ICMS
        "",                                                  # 109. Codigo do Motivo do Ressarcimento
        "",                                                  # 110. Chave Eletronica Emitida Pelo Substituto
        "",                                                  # 111. Participante Ret. ICMS ST
        "",                                                  # 112. Numero do Doc. Ret. ICMS ST
        "",                                                  # 113. Serie Doc. Ret. ICMS ST
        "",                                                  # 114. Cod. Item Ressarcimento Ret. ICMS ST
        "",                                                  # 115. Cod. Documento de Arrecadação
        "",                                                  # 116. Numero do DOC. de Arrecadação
        "",                                                  # 117. Base de Calculo de Ajuste de ICMS
        "",                                                  # 118. Aliquota de Ajuste de ICMS
        "",                                                  # 119. Valor de Ajuste de ICMS
        "",                                                  # 120. Aliquota do ICMS Diferimento
        "N",                                                 # 121. Decreto 46.303/2018(PE)
        "",                                                  # 122. Valor ICMS Substituto
        "",                                                  # 123. ICMS Efetivo
        "N",                                                 # 124. Decreto 20.686/99(AM)
    ]

    return "|".join(campos) + "|"