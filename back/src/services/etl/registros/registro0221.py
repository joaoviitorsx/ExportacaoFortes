import pandas as pd

class Registro0221Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.tabela = "registro_0221"
        self.nome = "0221"

    def set_context(self, periodo, filial):
        self.periodo = periodo
        self.filial = filial
    
    def processar(self, partes: list[str], cod_item_pai: str):
        if not self.periodo:
            raise ValueError("Contexto do período não definido para registro 0221.")

        partes = (partes + [None] * 2)[:2]

        dados = {
            "empresa_id": self.empresa_id,
            "periodo": self.periodo,
            "reg": partes[0],
            "cod_item": cod_item_pai,        
            "cod_item_atomico": partes[1],
            "ativo": True
        }

        if dados["cod_item_atomico"]:
            self.lote.append(dados)

    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
