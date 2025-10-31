def gerar_doc_key(dados: dict) -> str:
    """
    Gera uma chave única e padronizada para identificar documentos fiscais (nota fiscal).
    A prioridade é a CHV_NFE (chave de acesso da NF-e). 
    Caso não exista, usa uma composição determinística dos principais campos da nota.
    
    Campos usados no fallback:
      - CNPJ do emitente (ou destinatário, conforme IND_EMIT)
      - COD_MOD (modelo do documento)
      - SER (série)
      - NUM_DOC (número da nota)
      - DT_DOC (data de emissão)

    
    Retorna:
        str: chave única no formato "CHV_<chv_nfe>" ou "DOC_<cnpj>-<cod_mod>-<serie>-<num_doc>-<dt_doc>"
    """
    chv_nfe = str(dados.get("chv_nfe", "")).strip()
    if chv_nfe and len(chv_nfe) == 44:
        return f"CHV_{chv_nfe}"

    cnpj = (str(dados.get("cnpj", "")).replace(".", "").replace("/", "").replace("-", "").zfill(14))
    cod_mod = str(dados.get("cod_mod", "00")).zfill(2)
    serie = str(dados.get("ser", "0")).zfill(3)
    num_doc = str(dados.get("num_doc", "0")).zfill(9)
    dt_doc = str(dados.get("dt_doc", "")).replace("/", "").replace("-", "")

    if not dt_doc:
        dt_doc = "00000000"

    chave = f"DOC_{cnpj}-{cod_mod}-{serie}-{num_doc}-{dt_doc}"
    return chave
