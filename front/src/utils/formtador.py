def normalizarEmpresa(nome: str, cnpj: str):
        nome_val = (nome or "").strip()
        cnpj_val = "".join(filter(str.isdigit, cnpj or ""))[:14]
        if not cnpj_val and nome_val:
            import re
            m = re.search(r"(\d{14})", nome_val)
            if m:
                cnpj_val = m.group(1)
                nome_val = (nome_val.replace(cnpj_val, "").replace(" - ", " ").strip()).strip("- ").strip()
        return nome_val, cnpj_val