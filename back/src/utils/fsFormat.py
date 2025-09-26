import re
import unicodedata
from typing import Dict, Any
from datetime import date

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

#Formata um objeto date para YYYYMMDD. Retorna vazio se a data for nula.
def formatarData(value: Any) -> str:
    if isinstance(value, date):
        return value.strftime('%Y%m%d')
    return ''

#Mapeia o indicador de operação do SPED para o layout Fortes.
def tipoOperacao(ind_oper: str) -> str:
    return 'E' if ind_oper == '0' else 'S' if ind_oper == '1' else ''

#Mapeia o código do modelo do SPED para o layout Fortes.
def modeloDoc(cod_mod: str) -> str:
    modelos = {'55': 'NFE', '01': 'NF'}
    return modelos.get(cod_mod, '')

#Mapeia o código de situação do SPED para o layout Fortes.
def situacaoDoc(cod_sit: str) -> str:
    situacoes = {'00': 'N', '02': 'C', '03': 'E', '04': 'D', '05': 'I'}
    return situacoes.get(cod_sit, 'N') # Padrão 'N' de Normal