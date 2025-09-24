from typing import Tuple, List, Any
from datetime import date
from src.utils.sanitizacao import corrigirCfop, corrigirCstIcms

class ValidadorService:
    @staticmethod
    def validarRegistro0000(registro: dict) -> Tuple[bool, List[str]]:
        erros = []
        if not registro.get("cnpj") and not registro.get("cpf"):
            erros.append("Registro 0000 deve ter CNPJ ou CPF.")
        if not isinstance(registro.get("dt_ini"), date) or not isinstance(registro.get("dt_fin"), date):
            erros.append("Datas de início e fim inválidas no 0000.")
        return (len(erros) == 0, erros)

    @staticmethod
    def validarRegistro0150(registro: dict) -> Tuple[bool, List[str]]:
        erros = []
        if not registro.get("cod_part"):
            erros.append("0150 sem código do participante.")
        if not registro.get("nome"):
            erros.append("0150 sem nome do participante.")
        return (len(erros) == 0, erros)

    @staticmethod
    def validarRegistro0200(registro: dict) -> Tuple[bool, List[str]]:
        erros = []
        if not registro.get("cod_item"):
            erros.append("0200 sem código de item.")
        if not registro.get("descr_item"):
            erros.append("0200 sem descrição de item.")
        if not registro.get("cod_ncm"):
            erros.append("0200 sem código NCM.")
        return (len(erros) == 0, erros)

    @staticmethod
    def validarRegistroC100(registro: dict) -> Tuple[bool, List[str]]:
        erros = []
        if not registro.get("num_doc"):
            erros.append("C100 sem número de documento.")
        if not isinstance(registro.get("dt_doc"), date):
            erros.append("C100 sem data válida do documento.")
        return (len(erros) == 0, erros)

    @staticmethod
    def validarRegistroC170(registro: dict) -> Tuple[bool, List[str]]:
        erros = []
        if not registro.get("num_doc"):
            erros.append("C170 sem num_doc.")
        if not registro.get("num_item"):
            erros.append("C170 sem num_item.")
        if not registro.get("cfop") or not corrigirCfop(registro.get("cfop")):
            erros.append(f"CFOP inválido: {registro.get('cfop')}")
        if not registro.get("cst_icms") or not corrigirCstIcms(registro.get("cst_icms")):
            erros.append(f"CST ICMS inválido: {registro.get('cst_icms')}")
        return (len(erros) == 0, erros)

    @staticmethod
    def validarRegistroC190(registro: dict) -> Tuple[bool, List[str]]:
        erros = []
        if not registro.get("num_doc"):
            erros.append("C190 sem num_doc.")
        if not registro.get("cfop") or not corrigirCfop(registro.get("cfop")):
            erros.append(f"CFOP inválido: {registro.get('cfop')}")
        return (len(erros) == 0, erros)