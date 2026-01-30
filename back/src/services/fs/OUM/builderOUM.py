from ....utils.fsFormat import validacaoText, formatarValor

def builderOUM(dados: dict) -> str:
    fator = dados.get("fat_conv")

    # Validação: fator de conversão deve ser > 0
    # Se for None, vazio ou zero, usar 1.000 como padrão
    if fator is None or fator == "" or float(fator or 0) <= 0:
        fator = 1.0

    fator_str = formatarValor(fator, 3) or "1.000"

    campos = [
        "OUM",
        validacaoText(dados.get("cod_item"), 9),
        validacaoText(dados.get("unid_conv"), 6),
        fator_str,
    ]

    return "|".join(campos) + "|"
