import re
import unicodedata

UNIDADES = {
    "KG": "QUILOGRAMA",
    "UN": "UNIDADE",
    "PC": "PECA",
    "CX": "CAIXA",
    "L": "LITRO",
    "M": "METRO",
    "M2": "METRO QUADRADO",
    "M3": "METRO CUBICO",
    "PÇ": "PEÇA",
    "PCT": "PACOTE",
    "PR": "PAR",
    "DZ": "DUZIA",
    "GL": "GALÃO",
    "FR": "FRASCO",
    "ML": "MILILITRO",
}

def digitos(s):
    return re.sub(r"\D+", "", str(s or ""))

def removerAcentos(s):
    if not s:
        return ''
    return ''.join(c for c in unicodedata.normalize('NFKD', str(s)) if not unicodedata.combining(c))

def validacaoText(val, maxlen):
    return removerAcentos(str(val or '').replace('\n', ' ').replace('\r', ' ').strip())[:maxlen]