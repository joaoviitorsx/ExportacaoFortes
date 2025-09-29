import pandas as pd

from .....src.services.etl.validadorService import ValidadorService
from .....src.utils.sanitizacao import calcularPeriodo, formatarData

class Registro0000Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.filial = None
        self.tabela="registro_0000"

    def set_context(self, dt_ini, filial=None):
        self.periodo = calcularPeriodo(dt_ini)
        self.filial = filial

    def processar(self, partes: list[str]):
        partes = (partes + [None] * 15)[:15]

        dt_ini = formatarData(partes[3])
        dt_fin = formatarData(partes[4])
        cnpj = partes[6]
        self.filial = cnpj[8:12] if cnpj and len(cnpj) >= 12 else "0000"
        self.periodo = calcularPeriodo(partes[3])

        dados = {
            "reg": partes[0],
            "cod_ver": partes[1],
            "cod_fin": partes[2],
            "dt_ini": dt_ini,
            "dt_fin": dt_fin,
            "nome": partes[5],
            "cnpj": cnpj,
            "cpf": partes[7],
            "uf": partes[8],
            "ie": partes[9],
            "cod_num": partes[10],
            "im": partes[11],
            "suframa": partes[12],
            "ind_perfil": partes[13],
            "ind_ativ": partes[14],
            "filial": self.filial,
            "periodo": self.periodo,
            "empresa_id": self.empresa_id,
            "ativo": True
        }
        ok, erros = ValidadorService.validarRegistro0000(dados)
        if ok:
            self.lote.append(dados)
        else:
            return

        #self.lote.append(dados)

    def get_context(self):
        return {
            "filial": self.filial, 
            "periodo": self.periodo,
        }
    
    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
