import pandas as pd
from src.utils.siglas import obterUF
from src.services.etl.validadorService import ValidadorService

class Registro0150Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.filial = None
        self.tabela = "registro_0150"

    def set_context(self, periodo, filial=None):
        self.periodo = periodo
        self.filial = filial

    def processar(self, partes: list[str]):
        if not self.periodo:
            raise ValueError("Contexto do período não definido para registro 0150.")

        partes = (partes + [None] * 13)[:13]

        cod_mun = partes[7]
        cod_uf = cod_mun[:2] if cod_mun and len(cod_mun) >= 2 else None
        uf = obterUF(cod_uf)
        cnpj = partes[4]
        pj_pf = "F" if not cnpj else "J"

        dados = {
            "reg": partes[0],
            "cod_part": partes[1],
            "nome": partes[2],
            "cod_pais": partes[3],
            "cnpj": cnpj,
            "cpf": partes[5],
            "ie": partes[6],
            "cod_mun": cod_mun,
            "suframa": partes[8],
            "ende": partes[9],
            "num": partes[10],
            "compl": partes[11],
            "bairro": partes[12],
            "uf": uf,
            "tipo_pessoa": pj_pf,
            "periodo": self.periodo,
            "empresa_id": self.empresa_id,
            "ativo": True
        }

        ok, erros = ValidadorService.validarRegistro0150(dados)
        if ok:
            self.lote.append(dados)
        else:
            return
        
        #self.lote.append(dados)

    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
