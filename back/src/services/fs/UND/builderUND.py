from src.utils.fsFormat import validacaoText, UNIDADES

def builderUND(unidade_sigla: str) -> str:
    descricao = UNIDADES.get(unidade_sigla.upper(), unidade_sigla.upper())

    campos = [
        "UND",
        validacaoText(unidade_sigla, 6),
        validacaoText(descricao, 60)
    ]

    return "|".join(map(str, campos))