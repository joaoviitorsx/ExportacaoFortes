import pandas as pd
from .....src.utils.fsFormat import parseFator

class Registro0220Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.tabela = "registro_0220"
        self.nome = "0220"

    def set_context(self, periodo, filial):
        self.periodo = periodo
        self.filial = filial
    
    def processar(self, partes: list[str], cod_item: str):
        if not self.periodo:
            raise ValueError("Contexto do período não definido para registro 0220.")

        partes = (partes + [None] * 4)[:4]

        dados = {
            "empresa_id": self.empresa_id,
            "periodo": self.periodo,
            "reg": partes[0],
            "cod_item": cod_item,    
            "unid_conv": partes[1],
            "fat_conv": parseFator(partes[2]),
            "cod_barra": partes[3],
            "ativo": True
        }

        if dados["unid_conv"]:
            self.lote.append(dados)

    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
