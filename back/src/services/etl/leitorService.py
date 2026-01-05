import os
from typing import Dict, Any
from ....src.services.etl.registros.registro0000 import Registro0000Service
from ....src.services.etl.registros.registro0150 import Registro0150Service
from ....src.services.etl.registros.registro0200 import Registro0200Service
from ....src.services.etl.registros.registroC100 import RegistroC100Service
from ....src.services.etl.registros.registroC170 import RegistroC170Service
from ....src.services.etl.registros.registroC190 import RegistroC190Service
from ....src.services.etl.registros.registro0190 import Registro0190Service
from ....src.services.etl.registros.registro0221 import Registro0221Service
from ....src.services.etl.registros.registro0220 import Registro0220Service

from ....src.utils.key import docKey

class LeitorService:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

        self.s0000 = Registro0000Service(session, empresa_id)
        self.s0150 = Registro0150Service(session, empresa_id)
        self.s0190 = Registro0190Service(session, empresa_id)
        self.s0200 = Registro0200Service(session, empresa_id)
        self.s0220 = Registro0220Service(session, empresa_id)
        self.s0221 = Registro0221Service(session, empresa_id)
        self.sC100 = RegistroC100Service(session, empresa_id)
        self.sC170 = RegistroC170Service(session, empresa_id)
        self.sC190 = RegistroC190Service(session, empresa_id)

        self.contexto = None

    def lerArquivo(self, caminho: str) -> Dict[str, Any]:
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        resultado = {
            "cabecalhos": {"0000": [], "0150": [], "0190": [], "0200": [], "0220": [], "0221": []},
            "notas": []
        }

        encodings = ["latin-1", "utf-8", "utf-16", "cp1252"]
        for enc in encodings:
            try:
                with open(caminho, "r", encoding=enc, errors="ignore") as f:
                    self._processarLinhas(f, resultado)
                break
            except UnicodeDecodeError:
                continue

        return resultado

    def _processarLinhas(self, arquivo, resultado: Dict):
        nota_atual = None

        for linha in arquivo:
            campos = linha.strip().split("|")[1:-1]
            if len(campos) < 2:
                continue

            tipo = campos[0].upper()

            try:
                # Cabeçalhos
                if tipo == "0000":
                    self.s0000.processar(campos)
                    self.contexto = self.s0000.get_context()

                    for s in [self.s0150, self.s0190, self.s0200, self.s0220, self.s0221, self.sC100, self.sC170, self.sC190]:
                        s.set_context(self.contexto["periodo"], self.contexto["filial"])

                    resultado["cabecalhos"]["0000"].extend(self.s0000.lote)
                    self.s0000.lote.clear()

                elif tipo == "0150":
                    self.s0150.processar(campos)

                elif tipo == "0190":
                    self.s0190.processar(campos)

                elif tipo == "0200":
                    self.s0200.processar(campos)

                elif tipo == "0220":
                    cod_item_atual = self.s0200.cod_item_atual
                    if cod_item_atual:
                        self.s0220.processar(campos, cod_item_atual)

                elif tipo == "0221":
                    cod_item_atual = self.s0200.cod_item_atual
                    if cod_item_atual:
                        self.s0221.processar(campos, cod_item_atual) 

                # Documentos Fiscais
                elif tipo == "C100":
                    if nota_atual:
                        resultado["notas"].append(nota_atual)

                    c100_dados = self.sC100.processar(campos)
                    if c100_dados:
                        c100_dados["doc_key"] = docKey(c100_dados)
                        c100_dados["empresa_id"] = self.empresa_id
                        nota_atual = {"c100": c100_dados, "c170": [], "c190": []}
                    else:
                        nota_atual = None

                elif tipo == "C170" and nota_atual:
                    c170_dados = self.sC170.processar(campos, num_doc=None)
                    if c170_dados:
                        c170_dados["doc_key"] = nota_atual["c100"]["doc_key"]
                        c170_dados["empresa_id"] = self.empresa_id
                        nota_atual["c170"].append(c170_dados)

                elif tipo == "C190" and nota_atual:
                    c190_dados = self.sC190.processar(campos, num_doc=None)
                    if c190_dados:
                        c190_dados["doc_key"] = nota_atual["c100"]["doc_key"]
                        c190_dados["empresa_id"] = self.empresa_id
                        nota_atual["c190"].append(c190_dados)

            except Exception:
                continue

        # Adicionar última nota e cabeçalhos restantes
        if nota_atual:
            resultado["notas"].append(nota_atual)

        resultado["cabecalhos"]["0150"].extend(self.s0150.lote)
        resultado["cabecalhos"]["0190"].extend(self.s0190.lote)
        resultado["cabecalhos"]["0200"].extend(self.s0200.lote)
        resultado["cabecalhos"]["0220"].extend(self.s0220.lote)
        resultado["cabecalhos"]["0221"].extend(self.s0221.lote)
