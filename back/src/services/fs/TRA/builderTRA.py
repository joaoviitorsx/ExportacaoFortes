def builderTRA(quantidade_total_linhas: int) -> str:
    campos = [
        "TRA",
        quantidade_total_linhas
    ]
    
    return "|".join(map(str, campos))