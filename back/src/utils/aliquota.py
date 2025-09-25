import re
import pandas as pd

def categoriaAliquota(aliquota):
        if not aliquota:
            return 'regraGeral'
        aliquota_str = str(aliquota).upper().strip()
        aliquota_str = re.sub(r'[^\d.,A-Z]', '', aliquota_str)
        tokens_st = {"ISENTO", "ST", "SUBSTITUICAO", "PAUTA", "0", "0,00", "0.00"}
        if aliquota_str in tokens_st:
            return 'ST'
        try:
            aliquota_normalizada = aliquota_str.replace(',', '.')
            aliquota_num = float(aliquota_normalizada)
            if abs(aliquota_num - 17.00) <= 0.01 or abs(aliquota_num - 12.00) <= 0.01 or abs(aliquota_num - 4.00) <= 0.01:
                return '20RegraGeral'
            elif abs(aliquota_num - 5.95) <= 0.01 or abs(aliquota_num - 4.20) <= 0.01 or abs(aliquota_num - 1.54) <= 0.01:
                return '7CestaBasica'
            elif abs(aliquota_num - 10.20) <= 0.01 or abs(aliquota_num - 7.20) <= 0.01 or abs(aliquota_num - 2.63) <= 0.01:
                return '12CestaBasica'
            elif abs(aliquota_num - 37.80) <= 0.01 or abs(aliquota_num - 30.39) <= 0.01 or abs(aliquota_num - 8.13) <= 0.01:
                return '28BebidaAlcoolica'
            else:
                return 'regraGeral'
        except (ValueError, TypeError):
            return 'regraGeral'
        
def validarAliquota(v):
            if pd.isna(v) or str(v).strip() == "":
                return False
            v = str(v).strip().upper()
            if v in ["ISENTO", "ST"]:
                return True
            try:
                float(v.replace(",", "."))
                return True
            except ValueError:
                return False