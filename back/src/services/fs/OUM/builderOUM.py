from ....utils.fsFormat import validacaoText

def builderOUM(dados: dict) -> str:
    tipo = "OUM"
    cod_item = validacaoText(dados.get("cod_item", ""), 9)
    unid_inv = validacaoText(dados.get("unid_inv", ""), 6)
    unid_equiv = "1.000"  # Fixo conforme especificação

    campos = [
        tipo,        # 1. Tipo de Registro
        cod_item,    # 2. Código do Produto
        unid_inv,    # 3. Unidade de Medida
        unid_equiv,  # 4. Unidade Equivalente Padrão
    ]
    
    return "|".join(campos) + "|"