import re
import unicodedata
from typing import Dict, Any
from datetime import date, datetime

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
    "B1": "BANDEJA",
    "BAN": "BAN",
    "BD": "BD",
    "BDJ": "BANDEJA",
    "BJ": "BJ",
    "CA": "CARTELA",
    "CD": "UNIDADE",
    "CE": "CE",
    "CJ": "CONJUNTO",
    "CL": "CARTELA",
    "CP": "CP",
    "CR": "",
    "CRT": "CARTELA",
    "CT": "CARTELA",
    "CTC": "CARTUCHO",
    "CXA": "CAIXA",
    "CXT": "CAIXA",
    "DI": "DISPLAY",
    "DP": "DISPLAY",
    "DUZ": "DUZIA",
    "DZ": "DZ",
    "EE": "",
    "EM": "EMBALAGEM",
    "EQ": "",
    "EV": "ENVELOPE",
    "EXB": "EXB",
    "FAR": "FARDO",
    "FC": "FC",
    "FD": "FD",
    "FDO": "FARDO",
    "FR": "FR",
    "GA": "GARRAFA",
    "GF": "GARRAFA",
    "GL": "GALAO",
    "JG": "JG",
    "KI": "KIT",
    "LA": "LA",
    "LI": "LITRO",
    "LT": "LT",
    "LTA": "LATA",
    "MC": "MC",
    "MI": "MILHEIRO",
    "MIL": "MILHEIRO",
    "ML": "MILILITRO",
    "MT": "MT",
    "PA": "",
    "PAC": "PAC",
    "PAR": "PAR",
    "PC": "PC",
    "PCT": "PCT",
    "PO": "UNIDADE",
    "PR": "PAR",
    "PRD": "UNIDADE PADRAO",
    "PT": "PT",
    "RL": "ROLO",
    "SA": "UNIDADE",
    "SAC": "SACA",
    "SC": "UNIDADE",
    "SH": "UNIDADE",
    "TB": "CAIXA",
    "TP": "TIRA",
    "UD": "",
    "UNI": "UNIDADE",
    "VD": "VIDRO",
}

def digitos(s):
    return re.sub(r"\D+", "", str(s or ""))

def removerAcentos(s):
    if not s:
        return ''
    return ''.join(c for c in unicodedata.normalize('NFKD', str(s)) if not unicodedata.combining(c))

def validacaoText(val, maxlen):
    return removerAcentos(str(val or '').replace('\n', ' ').replace('\r', ' ').strip())[:maxlen]

from typing import Any

def formatarValor(value: Any, precision: int = 2) -> str:
    if value is None or value == '':
        return ''
    
    try:
        numeric_value = float(value)
        if numeric_value == 0.0:
            return ''
        return f'{numeric_value:.{precision}f}'.replace(',', '.')
        
    except (ValueError, TypeError):
        return str(value)

#Define o código de Tributação ICMS (Campo 11 do PNM) com base no CSTB.
def tributacaoICMS(cstb: str, aliquota_cadastro: str) -> str:
    # 1. Prioridade: Verifica a informação do cadastro de produtos
    aliquota_str = str(aliquota_cadastro).strip().upper()
    if aliquota_str == 'ST':
        return '3'  # Substituição Tributária
    if aliquota_str == 'ISENTO' or aliquota_str == 'I':
        return '4'  # Isenta

    # 2. Se não for um código, usa a lógica padrão baseada no CST
    if cstb in ('10', '30', '60', '70', '90'):
        return '3'  # Substituição Tributária
    if cstb == '20':
        return '2'  # Redução na Base de Cálculo
    if cstb in ('40', '41', '50'):
        return '4'  # Isenta
    if cstb == '51':
        return '5'  # Diferimento
    
    return '1'  # Padrão: Tributado Integralmente

#Formata um objeto date para YYYYMMDD. Retorna vazio se a data for nula.
def formatarData(value: Any) -> str:
    if isinstance(value, date):
        return value.strftime('%Y%m%d')
    return ''

#Mapeia o indicador de operação do SPED para o layout Fortes.
def tipoOperacao(ind_oper: str) -> str:
    return 'E' if ind_oper == '0' else 'S' if ind_oper == '1' else ''

def documentoProprio(ind_emit: str) -> str:
    return 'S' if ind_emit == '0' else 'N'

#Mapeia o código do modelo do SPED para o layout Fortes.
def modeloDoc(cod_mod: str) -> str:
    modelos = {'01': 'NF1', '1B': 'NF1A', '04': 'NFP', '55': 'NFE'}
    return modelos.get(cod_mod, '')

#Mapeia o código de situação do SPED para o layout Fortes.
def situacaoDoc(cod_sit: str) -> str:
    situacoes = {'00': '0', '01': '8', '02': '1', '03': '1', '04': '4', '05': '5'}
    return situacoes.get(cod_sit, '0')

def tipoFrete(ind_frt: str) -> str:
    fretes = {'0': 'R', '1': 'D', '9': 'N'}
    return fretes.get(ind_frt, 'N')

def tipoFatura(ind_pgto: str) -> str:
    if ind_pgto == '0':
        return 'V'  # A vista
    if ind_pgto == '1':
        return 'P'  # A prazo
    return 'N'  # Não informado/Outros

def normalizarDados(dados, nome_secao: str):
        if not dados:
            print(f"[WARNING] {nome_secao}: Nenhum dado retornado")
            return []
        
        if isinstance(dados, str):
            return [dados]
        elif isinstance(dados, list):
            return dados
        elif isinstance(dados, dict):
            linhas = []
            for chave, valor in dados.items():
                if isinstance(valor, list):
                    linhas.extend(valor)
                elif isinstance(valor, str):
                    linhas.append(valor)
            return linhas
        else:
            print(f"[WARNING] {nome_secao}: Tipo de dados não reconhecido: {type(dados)}")
            return [str(dados)]
        
def adicionarLinhas(destino: list, origem):
    if not origem:
        return

    if isinstance(origem, dict):
        for valor in origem.values():
            adicionarLinhas(destino, valor)

    elif isinstance(origem, list):
        destino.extend(origem)
    
    elif isinstance(origem, str):
        destino.append(origem)

def parse_data_sped(valor: str):
    if not valor:
        return None

    valor = valor.strip().replace("-", "").replace("/", "")
    
    # Ignora se não tiver exatamente 8 dígitos
    if not re.fullmatch(r"\d{8}", valor):
        return None

    for fmt in ("%d%m%Y", "%Y%m%d"):
        try:
            return datetime.strptime(valor, fmt).date()
        except ValueError:
            continue

    print(f"[DEBUG] Data inválida detectada no SPED: '{valor}'")
    return None

#Converte valor para float com validação
def floatC100(valor):
    if valor is None or valor == '':
        return 0.0
    try:
        result = float(valor)
        # Validar range (evitar overflow)
        if result > 999999999.99 or result < -999999999.99:
            return 999999999.99 if result > 0 else -999999999.99
        return result
    except (ValueError, TypeError):
        return 0.0

#Escapa aspas simples em strings para evitar SQL injection
def escapeString (valor):
    if not valor:
        return ''
    # Remover caracteres de controle e escapar aspas
    valor_limpo = str(valor).replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return valor_limpo.replace("'", "''")