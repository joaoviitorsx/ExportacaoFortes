from src.utils.fsFormat import digitos, validacaoText

def builderPRO(produto_data: dict) -> str:
    campos = [
        "PRO",                                          # 1: Tipo de Registro
        validacaoText(produto_data.get("cod_item", ""), 9),   # 2: Código
        validacaoText(produto_data.get("descr_item", ""), 60),# 3: Descrição
        validacaoText(produto_data.get("cod_item", ""), 60),   # 4: Código Utilizado Estab.
        validacaoText(produto_data.get("cod_ncm", ""), 20),    # 5: Código NCM
        validacaoText(produto_data.get("unid_inv", ""), 6),   # 6: Unidade de Medida Padrão
        "",                                             # 7: Unidade Medida DIEF
        "",                                             # 8: Unidade Medida CENFOP
        "",                                             # 9: Classificação
        validacaoText(produto_data.get("cod_gen", ""), 3),    # 10: Grupo (do Gênero do SPED)
        "",                                             # 11: Gênero
        digitos(produto_data.get("cod_barra", "")),     # 12: Código de Barras
        "", "", "", "", "", "", "", "", "", "", "",      # 13 a 23: Campos sem fonte no 0200
        "N",                                            # 24: Produto Desativado
        "", "", "", "", "", "", "", "", "", "", "", "",  # 25 a 36: Campos sem fonte no 0200
        "", "", "", "",                                 # 37 a 40: Campos sem fonte no 0200
        validacaoText(produto_data.get("cest", ""), 7), # 41: Cód. CEST
        "",                                             # 42: Custo de Aquisição
        "N", "N", "N", "N", "N", "N",                   # 43 a 48: Flags do Simples Nacional
        "",                                             # 49: Apuração do PIS/COFINS
        "", "", "", "", "", "N"                         # 50 a 55: Campos sem fonte no 0200
    ]

    return "|".join(map(str, campos))