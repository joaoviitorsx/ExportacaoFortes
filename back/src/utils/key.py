def docKey(dados: dict) -> str:
    chv_nfe = str(dados.get("chv_nfe", "")).strip()
    if chv_nfe and len(chv_nfe) == 44:
        return f"{chv_nfe}"

    cnpj = (str(dados.get("cnpj", "")).replace(".", "").replace("/", "").replace("-", "").zfill(14))
    cod_mod = str(dados.get("cod_mod", "00")).zfill(2)
    serie = str(dados.get("ser", "0")).zfill(3)
    num_doc = str(dados.get("num_doc", "0")).zfill(9)
    dt_doc = str(dados.get("dt_doc", "")).replace("/", "").replace("-", "")

    if not dt_doc:
        dt_doc = "00000000"

    chave = f"{cnpj}-{cod_mod}-{serie}-{num_doc}-{dt_doc}"
    return chave
