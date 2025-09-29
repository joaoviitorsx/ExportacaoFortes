def builderINM(c190_data: dict, uf: str) -> str:
    def num(valor) -> float:
        try:
            return float(valor or 0)
        except (ValueError, TypeError):
            return 0.0

    valor_operacao = num(c190_data.get("vl_opr"))
    cfop = str(c190_data.get("cfop") or "")
    base_icms = num(c190_data.get("vl_bc_icms"))
    aliq_icms = num(c190_data.get("aliq_icms"))
    valor_icms = num(c190_data.get("vl_icms"))
    valor_ipi = num(c190_data.get("vl_ipi"))
    # No SPED, o C190 não detalha a base de cálculo do IPI,
    # então usaremos 0.0 como placeholder.
    base_ipi = 0.0
    isentas_ipi = 0.0
    outras_ipi = 0.0


    # --- CST ICMS (separa primeiro dígito do restante) ---
    cst_icms = str(c190_data.get("cst_icms") or "").zfill(3)  # força 3 dígitos
    csta = cst_icms[0]       # ex: "0"
    cstb = cst_icms[1:]      # ex: "10"

    # --- Tratamento de isentas e outras para ICMS ---
    isentas_icms = 0.0
    outras_icms = 0.0
    if cstb in ["40", "41"]:
        isentas_icms = valor_operacao
    elif cstb in ["50", "51", "90"]:
        outras_icms = valor_operacao

    # --- Montagem dos campos INM ---
    campos = [
        "INM",                       # 01 - Tipo de Registro
        f"{valor_operacao:.2f}",     # 02 - Valor Contábil
        uf,                          # 03 - UF
        cfop,                        # 04 - CFOP
        "",                          # 05 - CFOP p/ Transferência Automática
        f"{base_icms:.2f}",          # 06 - Base de Cálculo do ICMS
        f"{aliq_icms:.2f}",          # 07 - Alíquota do ICMS
        f"{valor_icms:.2f}",         # 08 - Valor do ICMS
        f"{isentas_icms:.2f}",       # 09 - Isentas do ICMS
        f"{outras_icms:.2f}",        # 10 - Outras do ICMS
        f"{base_ipi:.2f}",           # 11 - Base de Cálculo do IPI
        f"{valor_ipi:.2f}",          # 12 - Valor do IPI
        f"{isentas_ipi:.2f}",        # 13 - Isentas do IPI
        f"{outras_ipi:.2f}",         # 14 - Outras do IPI
        "N", "N", "N", "N",          # 15 a 18 - Indicadores Diversos
        csta,                        # 19 - CST A
        cstb,                        # 20 - CST B
        "", "", "",                  # 21 a 23 - Reservado
        "N", "N", "N",               # 24 a 26 - Indicadores
        "",                          # 27 - Reservado
        f"{0.0:.2f}", f"{0.0:.2f}",  # 28 a 29 - Reservado
        f"{0.0:.2f}", f"{0.0:.2f}",  # 30 a 31 - Reservado
        f"{0.0:.2f}", f"{0.0:.2f}",  # 32 a 33 - Reservado
        f"{0.0:.2f}",                # 34 - Reservado
    ]

    return "|".join(map(str, campos))