import re
from datetime import datetime, date
from typing import Optional

# regex pré-compiladas
RE_NUMERO = re.compile(r"^\d+([,\.]\d+)?$")
RE_UNIDADE_ALFA = re.compile(r"^([A-Za-z]+)(\d+)?$")

TAMANHOS_MAXIMOS = {
    "unid": 2,
    "cod_item": 60,
    "descr_item": 255,
    "descr_compl": 255,
    "cod_nat": 11,
    "cod_cta": 255,
    "cod_part": 60,
    "nome": 100,
}

def limparAliquota(valor: Optional[str]) -> Optional[float]:
    if not valor:
        return None
    s = str(valor).strip().replace("%", "").replace(",", ".")
    try:
        num = float(s)
        return 0.0 if num == 0 else round(num, 2)
    except ValueError:
        v = s.upper()
        if v in {"ST", "ISENTO", "PAUTA"}:
            return v
        return None

def truncar(valor, limite):
    if valor is None:
        return None
    return str(valor).strip()[:limite]

def corrigirUnidade(valor):
    if not valor:
        return "UN"
    s = str(valor).strip().upper()
    if RE_NUMERO.match(s):
        return "UN"
    m = RE_UNIDADE_ALFA.match(s)
    if m:
        return m.group(1)[:3]
    return s[:3] if len(s) > 3 else s

def corrigirCstIcms(valor: Optional[str]) -> Optional[str]:
    if not valor:
        return "00"
    s = str(valor).strip().replace(",", ".")
    if s.replace(".", "").isdigit():
        try:
            return str(int(float(s))).zfill(2)[:2]
        except ValueError:
            return "00"
    return s[:2] if s[:2].isdigit() else "00"

def corrigirCfop(valor: Optional[str]) -> Optional[str]:
    if not valor:
        return None
    s = re.sub(r"\D", "", str(valor))
    if len(s) != 4:
        return None
    return s

def corrigirIndMov(valor):
    return str(valor)[0] if valor else "0"

def validarEstruturaC170(dados: list) -> bool:
    try:
        if not dados or len(dados) < 43:
            return False
        return all([dados[0], dados[39], dados[40]])
    except Exception:
        return False

def sanitizarCampo(campo, valor):
    def _numero(v):
        if v is None or v == "":
            return None
        try:
            return float(str(v).replace(",", "."))
        except ValueError:
            return None

    regras = {
        "cod_item": lambda v: truncar(v, 60),
        "descr_item": lambda v: truncar(v, 255),
        "descr_compl": lambda v: truncar(v, 255),
        "cod_cta": lambda v: truncar(v, 255),
        "cod_nat": lambda v: truncar(v, 11),
        "cod_part": lambda v: truncar(v, 60),
        "nome": lambda v: truncar(v, 100),
        "reg": lambda v: truncar(v, 4),

        "unid": corrigirUnidade,
        "unid_inv": corrigirUnidade,
        "ind_mov": corrigirIndMov,
        "cod_mod": lambda v: str(v).zfill(2)[:2] if v else "00",
        "cst_icms": corrigirCstIcms,
        "cfop": corrigirCfop,

        # numéricos
        "vl_item": _numero,
        "vl_desc": _numero,
        "vl_merc": _numero,
        "aliq_icms": _numero,
        "aliq_ipi": _numero,
        "aliq_pis": _numero,
        "aliq_cofins": _numero,
        "vl_bc_icms": _numero,
        "vl_icms": _numero,
        "vl_bc_ipi": _numero,
        "vl_ipi": _numero,
        "vl_bc_pis": _numero,
        "vl_pis": _numero,
        "vl_bc_cofins": _numero,
        "vl_cofins": _numero,
        "vl_abat_nt": _numero,
        "quant_bc_pis": _numero,
        "quant_bc_cofins": _numero,
        "aliq_pis_reais": _numero,
        "aliq_cofins_reais": _numero,
    }
    try:
        return regras.get(campo, lambda v: v)(valor)
    except Exception:
        return None

def sanitizarRegistro(registro_dict: dict) -> dict:
    return {campo: sanitizarCampo(campo, valor) for campo, valor in registro_dict.items()}

def calcularPeriodo(dt_ini_0000: str) -> str:
    if not dt_ini_0000 or len(dt_ini_0000) < 6:
        return "00/0000"
    return f"{dt_ini_0000[2:4]}/{dt_ini_0000[4:]}"

def formatarData(data_str: str) -> Optional[date]:
    if not data_str or len(data_str) != 8:
        return None
    try:
        return datetime.strptime(data_str, "%d%m%Y").date()
    except ValueError:
        return None

def parseDecimal(valor: str) -> Optional[float]:
    if not valor:
        return None
    try:
        return float(str(valor).replace(",", "."))
    except ValueError:
        return None

def parseDate(valor: str):
    if not valor or len(valor) != 8:
        return None
    try:
        return datetime.strptime(valor, "%d%m%Y").date()
    except ValueError:
        return None