from ....utils.fsFormat import validacaoText

def builderUND(cod_unid: str, descr_unid: str) -> str:
    campos = [
        "UND",
        validacaoText(cod_unid, 6),
        validacaoText(descr_unid, 60),
    ]

    return "|".join(campos)
