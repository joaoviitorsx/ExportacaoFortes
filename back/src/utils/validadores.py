import os
import re

def removedorCaracteres(valor: str) -> str:
    return re.sub(r'\D', '', valor)

def validarCnpj(cnpj: str) -> bool:
    cnpj = removedorCaracteres(cnpj)
    return len(cnpj) == 14 and cnpj.isdigit()

def formatarCnpj(value):
        digits = ''.join(filter(str.isdigit, value))
        if len(digits) <= 2:
            return digits
        elif len(digits) <= 5:
            return f"{digits[:2]}.{digits[2:]}"
        elif len(digits) <= 8:
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:]}"
        elif len(digits) <= 12:
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:]}"
        else:
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:14]}"

def validateCnpj(cnpj):
        digits = ''.join(filter(str.isdigit, cnpj))
        return len(digits) == 14

def formatador(valor):
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def formatarValor(value):
        cleaned = ''.join(c for c in value if c.isdigit() or c == ',')
        parts = cleaned.split(',')
        if len(parts) > 2:
            return parts[0] + ',' + ''.join(parts[1:])
        if len(parts) == 2 and len(parts[1]) > 2:
            return parts[0] + ',' + parts[1][:2]
        return cleaned

def validarSpedFiscal(arquivo: str) -> bool:
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

        if not arquivo.lower().endswith(".txt"):
            raise ValueError("Arquivo inválido: apenas arquivos .txt são aceitos.")

        encodings = ["latin-1", "utf-8", "utf-16", "cp1252"]
        linhas = None
        for enc in encodings:
            try:
                with open(arquivo, "r", encoding=enc) as f:
                    linhas = [l.strip() for _, l in zip(range(5000), f) if l.strip()]
                    break
            except (UnicodeDecodeError, StopIteration):
                continue
            except Exception as e:
                raise ValueError(f"Erro ao abrir o arquivo: {e}")

        if not linhas:
            raise ValueError("Arquivo inválido: não foi possível ler o conteúdo (arquivo corrompido ou codificação incorreta).")

        registros = ["|0000|", "|0150|", "|0200|", "|C100|", "|C170|", "|C190|"]

        faltantes = [r for r in registros if not any(l.startswith(r) for l in linhas)]

        if faltantes:
            faltantes_fmt = ", ".join(r.replace("|", "") for r in faltantes)
            raise ValueError(
                f"Arquivo inválido: faltam os registros obrigatórios {faltantes_fmt}. "
                "Verifique se o arquivo é realmente um SPED Fiscal EFD ICMS/IPI."
            )

        return True

