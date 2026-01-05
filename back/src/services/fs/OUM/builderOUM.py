from ....utils.fsFormat import validacaoText, formatarValor

def builderOUM(dados: dict) -> str:
    fator = dados.get("fat_conv")

    if fator is None or fator == "":
        fator = 0.0

    fator_str = formatarValor(fator, 3) or "0.000"

    campos = [
        "OUM",
        validacaoText(dados.get("cod_item"), 9),
        validacaoText(dados.get("unid_conv"), 6),
        fator_str,
    ]

    return "|".join(campos) + "|"
