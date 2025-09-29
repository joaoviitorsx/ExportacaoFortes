from ....utils.fsFormat import digitos, validacaoText

def builderPAR(dados: dict) -> str:
    tipo = "PAR"
    cod_part = validacaoText(dados.get("cod_part"), 9)
    nome = validacaoText(dados.get("nome"), 100).upper()
    uf = validacaoText(dados.get("uf"), 2).upper()

    doc = digitos(dados.get("cnpj")) or digitos(dados.get("cpf"))
    doc = doc[:14]

    # IE e IM
    ie = digitos(dados.get("ie"))[:14]
    im = validacaoText(dados.get("im"), 21)

    # Endereço e localização
    logradouro = validacaoText(dados.get("ende") or dados.get("end"), 60).upper()
    numero = validacaoText(dados.get("num"), 6)
    complemento = validacaoText(dados.get("compl"), 20).upper()
    bairro = validacaoText(dados.get("bairro"), 50).upper()
    cep = digitos(dados.get("cep"))[:8]
    email = validacaoText(dados.get("email"), 60)
    cnae = digitos(dados.get("cnae"))[:7]
    cod_mun = (digitos(dados.get("cod_mun")) or "")[-5:]

    # Dados fiscais
    suframa = validacaoText(dados.get("suframa"), 14)
    cod_pais = digitos(dados.get("cod_pais")) or "1058"
    cod_pais = cod_pais[:4]
    exterior = "S" if cod_pais != "1058" else "N"
    ind_icms = "1" if ie else "3"

    simples = str(dados.get("simples", "")).upper()
    if "MEI" in simples:
        situacao_trib = "2"
    elif "SIMPLES" in simples or "SN" in simples:
        situacao_trib = "1"
    else:
        situacao_trib = "0"

    campos = [
        tipo,                       # 1
        cod_part,                   # 2
        nome,                       # 3
        uf,                         # 4
        doc,                        # 5
        ie,                         # 6
        im,                         # 7
        "N",                        # 8 - Informa ISS Digital
        "N",                        # 9 - Informa DIEF
        "N",                        # 10 - Informa DIC
        "N",                        # 11 - Informa DEMMS
        "N",                        # 12 - Órgão Público
        "N",                        # 13 - Informa Livro Eletrônico
        "N",                        # 14 - Fornecedor de Prod. Primário
        "N",                        # 15 - Sociedade Simples
        "",                         # 16 - Tipo de Logradouro (vazio por padrão)
        logradouro,                 # 17 - Logradouro
        numero,                     # 18 - Número
        complemento,                # 19 - Complemento
        "",                         # 20 - Tipo de Bairro (vazio por padrão)
        bairro,                     # 21 - Bairro
        cep,                        # 22 - CEP
        cod_mun,                    # 23 - Município
        "",                         # 24 - DDD (vazio)
        "",                         # 25 - Telefone (vazio)
        suframa,                    # 26 - Suframa
        "N",                        # 27 - Substituto ISS
        "",                         # 28 - Conta (Remetente)
        "",                         # 29 - Conta (Destinatário)
        cod_pais,                   # 30 - País
        exterior,                   # 31 - Exterior
        ind_icms,                   # 32 - Indicador do ICMS
        email,                      # 33 - E-mail
        "N",                        # 34 - Hospitais
        "N",                        # 35 - Administradora
        cnae,                       # 36 - CNAE21
        "N",                        # 37 - CPRB
        situacao_trib,              # 38 - Situação Tributária
        "N",                        # 39 - Produtor Rural
        ""                          # 40 - Indicativo da Aquisição
    ]

    return "|".join(map(str, campos))
