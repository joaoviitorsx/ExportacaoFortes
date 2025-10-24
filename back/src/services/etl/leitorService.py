import os
import queue

from ....src.services.etl.registros.registro0000 import Registro0000Service
from ....src.services.etl.registros.registro0150 import Registro0150Service
from ....src.services.etl.registros.registro0200 import Registro0200Service
from ....src.services.etl.registros.registroC100 import RegistroC100Service
from ....src.services.etl.registros.registroC170 import RegistroC170Service
from ....src.services.etl.registros.registroC190 import RegistroC190Service

from ....src.utils.validadores import validarSpedFiscal

class LeitorService:
    def __init__(self, session, empresa_id, arquivos: list[str], fila: queue.Queue, buffer_size=10000):
        self.session = session
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        self.fila = fila
        self.buffer_size = buffer_size

        self.s0000 = Registro0000Service(session, empresa_id)
        self.s0150 = Registro0150Service(session, empresa_id)
        self.s0200 = Registro0200Service(session, empresa_id)
        self.sC100 = RegistroC100Service(session, empresa_id)
        self.sC170 = RegistroC170Service(session, empresa_id)
        self.sC190 = RegistroC190Service(session, empresa_id)

    contador = 0

    def executar(self):
        for arquivo in self.arquivos:
            self.processarArquivo(arquivo)

    def processarArquivo(self, arquivo):
        caminho = os.path.abspath(arquivo)

        if not os.path.exists(caminho):
            print(f"[ERRO] Arquivo não encontrado: {caminho}")
            return

        try:
            #validarSpedFiscal(arquivo)
            print(f"[INFO] Arquivo validado com sucesso: {os.path.basename(caminho)}")
        except ValueError as e:
            print(f"[ERRO] Arquivo inválido: {e}")
            return
        
        print(f"[INFO] Iniciando leitura do arquivo: {os.path.basename(caminho)}")
        c100Atual = None

        encodings = ["latin-1", "utf-8", "utf-16", "cp1252"]
        for enc in encodings:
            try:
                with open(arquivo, "r", encoding=enc) as f:
                    for linha in f:
                        campos = linha.strip().split("|")[1:-1]
                        if len(campos) < 2:
                            continue

                        tipo = campos[0].upper()

                        try:
                            if tipo == "0000":
                                self.s0000.processar(campos)
                                contexto = self.s0000.get_context()

                                # repassa contexto para todos os services
                                for s in [self.s0150, self.s0200, self.sC100, self.sC170, self.sC190]:
                                    s.set_context(contexto["periodo"], contexto["filial"])

                                if len(self.s0000.lote) >= self.buffer_size:
                                    self.enviarRegistros("0000", self.s0000.lote)

                            elif tipo == "0150":
                                self.s0150.processar(campos)
                                if len(self.s0150.lote) >= self.buffer_size:
                                    self.enviarRegistros("0150", self.s0150.lote)

                            elif tipo == "0200":
                                self.s0200.processar(campos)
                                if len(self.s0200.lote) >= self.buffer_size:
                                    self.enviarRegistros("0200", self.s0200.lote)

                            elif tipo == "C100":
                                c100Atual = self.sC100.processar(campos)
                                mapa = self.sC100.getDocumentos()
                                self.sC170.setDocumentos(mapa)
                                self.sC190.setDocumentos(mapa)

                                if len(self.sC100.lote) >= self.buffer_size:
                                    self.enviarRegistros("C100", self.sC100.lote)

                            elif tipo == "C170" and c100Atual:
                                self.sC170.processar(campos, num_doc=c100Atual["num_doc"])
                                if len(self.sC170.lote) >= self.buffer_size:
                                    self.enviarRegistros("C170", self.sC170.lote)

                            elif tipo == "C190" and c100Atual:  
                                self.sC190.processar(campos, num_doc=c100Atual["num_doc"])
                                if len(self.sC190.lote) >= self.buffer_size:
                                    self.enviarRegistros("C190", self.sC190.lote)

                        except Exception as e:
                            # print(f"[ERRO] Falha ao processar linha {tipo}: {e}")
                            continue
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"[ERRO] Falha ao abrir arquivo {arquivo}: {e}")
                continue

        self.enviarRegistros("0000", self.s0000.lote)
        self.enviarRegistros("0150", self.s0150.lote)
        self.enviarRegistros("0200", self.s0200.lote)
        self.enviarRegistros("C100", self.sC100.lote)
        self.enviarRegistros("C170", self.sC170.lote)
        self.enviarRegistros("C190", self.sC190.lote)

        print(f"[INFO] Leitura concluída: {os.path.basename(arquivo)}")

    def enviarRegistros(self, tipo, lote):
        if lote:
            prioridade = self.prioridade(tipo)
            LeitorService.contador += 1
            self.fila.put((prioridade, tipo,LeitorService.contador, lote.copy()))
            print(f"[DEBUG] Lote enviado: {tipo} ({len(lote)} registros)")
            lote.clear()

    def prioridade(self, tipo):
        if tipo in ["0000", "0150", "0200"]:
            return 1
        elif tipo == "C100":
            return 2
        else:  # C170, C190
            return 3