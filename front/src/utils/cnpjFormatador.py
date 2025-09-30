def formatarCnpj(valor: str) -> str:
    numeros = "".join(filter(str.isdigit, valor))[:14]

    if len(numeros) <= 2:
        return numeros
    elif len(numeros) <= 5:
        return f"{numeros[:2]}.{numeros[2:]}"
    elif len(numeros) <= 8:
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:]}"
    elif len(numeros) <= 12:
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:]}"
    else:
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"
