def normalizarEmpresa(nome: str, cnpj: str):
        import re

        nome_val = (nome or "").strip()
        cnpj_val = "".join(filter(str.isdigit, cnpj or ""))[:14]

        if not cnpj_val and nome_val:
            # Captura CNPJ com ou sem máscara
            m = re.search(r"(\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2})", nome_val)
            if m:
                cnpj_extraido = "".join(ch for ch in m.group(1) if ch.isdigit())[:14]
                if cnpj_extraido:
                    cnpj_val = cnpj_extraido
                    nome_val = nome_val.replace(m.group(1), " ").replace(" - ", " ")
                    nome_val = re.sub(r"\s+", " ", nome_val).strip().strip("- ").strip()

        return nome_val, cnpj_val
