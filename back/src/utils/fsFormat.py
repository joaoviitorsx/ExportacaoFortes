import re
import unicodedata
from typing import Dict, Any

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

def formatarValor(value: Any, precision: int = 2) -> str:
    if value is None or value == '':
        return ''
    try:
        return f'{float(value):.{precision}f}'.replace(',', '.')
    except (ValueError, TypeError):
        return str(value)

#Define o código de Tributação ICMS (Campo 11 do PNM) com base no CSTB.
def tributacaoICMS(cstb: str) -> str:
    if not cstb:
        return '1'
    if cstb in ('10', '30', '60', '70', '90'):
        return '3'  # Substituição Tributária
    if cstb == '20':
        return '2'  # Redução na Base de Cálculo
    if cstb in ('40', '41', '50'):
        return '4'  # Isenta
    if cstb == '51':
        return '5'  # Diferimento
    return '1'  # Tributado Integralmente (Default para 00, etc.)