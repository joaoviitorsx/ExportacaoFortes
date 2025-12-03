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
        raise ValueError("Apenas arquivos .txt são aceitos")

    # Tenta ler com diferentes encodings
    encodings = ["latin-1", "utf-8", "cp1252", "utf-16"]
    linhas = None
    
    for enc in encodings:
        try:
            with open(arquivo, "r", encoding=enc) as f:
                linhas = [l.strip() for l in f if l.strip()]
                break
        except (UnicodeDecodeError, StopIteration):
            continue
        except Exception as e:
            raise ValueError(f"Erro ao ler arquivo: {e}")

    if not linhas:
        raise ValueError("Arquivo vazio ou corrompido")

    # Valida formato pipe
    if not any("|" in linha for linha in linhas[:100]):
        raise ValueError("Formato inválido: arquivo deve ter campos separados por pipe (|)")

    # Valida primeira linha (deve ser 0000)
    if not linhas[0].startswith("|0000|"):
        raise ValueError("Formato inválido: arquivo deve começar com registro |0000|")

    # Registros obrigatórios
    registros_obrigatorios = ["|0000|", "|0150|", "|0200|", "|C100|", "|C170|", "|C190|"]
    faltantes = []
    
    for registro in registros_obrigatorios:
        if not any(linha.startswith(registro) for linha in linhas):
            faltantes.append(registro.replace("|", ""))

    if faltantes:
        raise ValueError(
            f"Registros obrigatórios faltando: {', '.join(faltantes)}"
        )

    return True