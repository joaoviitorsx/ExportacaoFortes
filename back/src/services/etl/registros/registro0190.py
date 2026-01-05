import pandas as pd

class Registro0190Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.tabela = "registro_0190"
        self.nome = "0190"

    def set_context(self, periodo, filial):
        self.periodo = periodo
        self.filial = filial
    
    def processar(self, partes: list[str]):
        if not self.periodo:
            raise ValueError("Contexto do período não definido para registro 0190.")

        partes = (partes + [None] * 3)[:3]

        dados = {
            "empresa_id": self.empresa_id,
            "periodo": self.periodo,
            "reg": partes[0],
            "unid": partes[1],
            "descr": partes[2],
            "ativo": True
        }
        # Validação simples: verificar se a unidade de medida está presente
        if dados["unid"]:
            self.lote.append(dados)
        else:
            return
        
    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)