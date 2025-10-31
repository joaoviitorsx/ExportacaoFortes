import os
from typing import List, Dict, Any, Optional
from ....src.services.etl.registros.registro0000 import Registro0000Service
from ....src.services.etl.registros.registro0150 import Registro0150Service
from ....src.services.etl.registros.registro0200 import Registro0200Service
from ....src.services.etl.registros.registroC100 import RegistroC100Service
from ....src.services.etl.registros.registroC170 import RegistroC170Service
from ....src.services.etl.registros.registroC190 import RegistroC190Service
from ....src.utils.key import gerar_doc_key


class LeitorService:
    """
    Leitor linear do arquivo SPED Fiscal.
    Processa linha por linha e monta estrutura hierárquica:
    C100 -> [C170, C170, ...], [C190, C190, ...]
    """

    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id

        # Services de parsing
        self.s0000 = Registro0000Service(session, empresa_id)
        self.s0150 = Registro0150Service(session, empresa_id)
        self.s0200 = Registro0200Service(session, empresa_id)
        self.sC100 = RegistroC100Service(session, empresa_id)
        self.sC170 = RegistroC170Service(session, empresa_id)
        self.sC190 = RegistroC190Service(session, empresa_id)

        # Contexto
        self.contexto = None

    def ler_arquivo(self, caminho: str) -> Dict[str, Any]:
        """
        Lê um arquivo SPED e retorna estrutura com todos os dados organizados.
        
        Retorna:
            {
                "cabecalhos": {
                    "0000": [...],
                    "0150": [...],
                    "0200": [...]
                },
                "notas": [
                    {
                        "c100": {...},
                        "c170": [{...}, {...}],
                        "c190": [{...}, {...}]
                    },
                    ...
                ]
            }
        """
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

        print(f"\n📄 Lendo arquivo: {os.path.basename(caminho)}")

        resultado = {
            "cabecalhos": {
                "0000": [],
                "0150": [],
                "0200": []
            },
            "notas": []
        }

        # Tentar múltiplos encodings
        encodings = ["latin-1", "utf-8", "utf-16", "cp1252"]
        for enc in encodings:
            try:
                with open(caminho, "r", encoding=enc) as f:
                    self._processar_linhas(f, resultado)
                print(f"✅ Encoding usado: {enc}")
                break
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"❌ Erro ao processar arquivo: {e}")
                raise

        return resultado

    def _processar_linhas(self, arquivo, resultado: Dict):
        """Processa linha por linha do arquivo SPED"""
        nota_atual = None
        linha_num = 0
        debug_primeira_nota = True
        
        # Contadores de debug
        count_c100 = 0
        count_c170_lidos = 0
        count_c170_processados = 0
        count_c190_lidos = 0
        count_c190_processados = 0

        for linha in arquivo:
            linha_num += 1
            campos = linha.strip().split("|")[1:-1]
            
            if len(campos) < 2:
                continue

            tipo = campos[0].upper()

            try:
                # ============================================
                # CABEÇALHOS
                # ============================================
                if tipo == "0000":
                    self.s0000.processar(campos)
                    self.contexto = self.s0000.get_context()
                    
                    # Propagar contexto
                    for s in [self.s0150, self.s0200, self.sC100, self.sC170, self.sC190]:
                        s.set_context(self.contexto["periodo"], self.contexto["filial"])
                    
                    resultado["cabecalhos"]["0000"].extend(self.s0000.lote)
                    self.s0000.lote.clear()
                    print(f"   🔧 Contexto definido: período={self.contexto['periodo']}, filial={self.contexto['filial']}")

                elif tipo == "0150":
                    self.s0150.processar(campos)

                elif tipo == "0200":
                    self.s0200.processar(campos)

                # ============================================
                # DOCUMENTOS FISCAIS
                # ============================================
                elif tipo == "C100":
                    count_c100 += 1
                    
                    # Salvar nota anterior ANTES de criar nova
                    if nota_atual:
                        resultado["notas"].append(nota_atual)
                        
                        # Debug da primeira nota
                        if debug_primeira_nota:
                            print(f"\n   [DEBUG] Primeira nota salva:")
                            print(f"      C100: num_doc={nota_atual['c100'].get('num_doc')}")
                            print(f"      C170: {len(nota_atual['c170'])} itens")
                            print(f"      C190: {len(nota_atual['c190'])} totalizadores")
                            if nota_atual['c170']:
                                print(f"      Primeiro C170: cod_item={nota_atual['c170'][0].get('cod_item')}")
                            else:
                                print(f"      ⚠️  NOTA SEM C170 - Possível problema no processamento!")
                            debug_primeira_nota = False
                    
                    # Nova nota
                    c100_dados = self.sC100.processar(campos)
                    
                    if c100_dados:
                        doc_key = gerar_doc_key(c100_dados)
                        c100_dados["doc_key"] = doc_key
                        c100_dados["empresa_id"] = self.empresa_id
                        
                        nota_atual = {
                            "c100": c100_dados,
                            "c170": [],
                            "c190": []
                        }
                    else:
                        nota_atual = None
                        print(f"   ⚠️  C100 linha {linha_num} retornou None")

                elif tipo == "C170":
                    count_c170_lidos += 1
                    
                    # *** DEBUG: Verificar se há C100 atual ***
                    if not nota_atual:
                        if count_c170_lidos <= 3:
                            print(f"   ⚠️  [LINHA {linha_num}] C170 sem C100 atual!")
                        continue
                    
                    # *** DEBUG: Mostrar campos do C170 ***
                    if count_c170_lidos <= 3:
                        print(f"\n   [DEBUG C170 #{count_c170_lidos}] Linha {linha_num}")
                        print(f"      Campos: {campos[:10]}...")  # Primeiros 10 campos
                    
                    c170_dados = self.sC170.processar(campos, num_doc=None)
                    
                    if c170_dados:
                        count_c170_processados += 1
                        c170_dados["doc_key"] = nota_atual["c100"]["doc_key"]
                        c170_dados["empresa_id"] = self.empresa_id
                        nota_atual["c170"].append(c170_dados)
                        
                        if count_c170_processados <= 3:
                            print(f"      ✅ Processado: cod_item={c170_dados.get('cod_item')}")
                    else:
                        if count_c170_lidos <= 3:
                            print(f"      ❌ processar() retornou None!")
                            print(f"      Campos recebidos: {len(campos)} campos")

                elif tipo == "C190":
                    count_c190_lidos += 1
                    
                    # *** DEBUG: Verificar se há C100 atual ***
                    if not nota_atual:
                        if count_c190_lidos <= 3:
                            print(f"   ⚠️  [LINHA {linha_num}] C190 sem C100 atual!")
                        continue
                    
                    # *** DEBUG: Mostrar campos do C190 ***
                    if count_c190_lidos <= 3:
                        print(f"\n   [DEBUG C190 #{count_c190_lidos}] Linha {linha_num}")
                        print(f"      Campos: {campos[:10]}...")
                    
                    c190_dados = self.sC190.processar(campos, num_doc=None)
                    
                    if c190_dados:
                        count_c190_processados += 1
                        c190_dados["doc_key"] = nota_atual["c100"]["doc_key"]
                        c190_dados["empresa_id"] = self.empresa_id
                        nota_atual["c190"].append(c190_dados)
                        
                        if count_c190_processados <= 3:
                            print(f"      ✅ Processado: cst_icms={c190_dados.get('cst_icms')}")
                    else:
                        if count_c190_lidos <= 3:
                            print(f"      ❌ processar() retornou None!")
                            print(f"      Campos recebidos: {len(campos)} campos")

            except Exception as e:
                print(f"⚠️ Erro linha {linha_num} ({tipo}): {e}")
                import traceback
                traceback.print_exc()
                continue

        # Salvar última nota
        if nota_atual:
            resultado["notas"].append(nota_atual)

        # Coletar cabeçalhos restantes
        resultado["cabecalhos"]["0150"].extend(self.s0150.lote)
        resultado["cabecalhos"]["0200"].extend(self.s0200.lote)

        # Estatísticas detalhadas
        total_c170 = sum(len(n["c170"]) for n in resultado["notas"])
        total_c190 = sum(len(n["c190"]) for n in resultado["notas"])
        notas_com_c170 = sum(1 for n in resultado["notas"] if n["c170"])
        notas_sem_c170 = len(resultado["notas"]) - notas_com_c170
        
        print(f"\n   📊 Estatísticas de leitura:")
        print(f"      📋 C100 lidos:            {count_c100}")
        print(f"      📄 C170 lidos:            {count_c170_lidos}")
        print(f"      ✅ C170 processados:      {count_c170_processados}")
        print(f"      ❌ C170 ignorados:        {count_c170_lidos - count_c170_processados}")
        print(f"      📄 C190 lidos:            {count_c190_lidos}")
        print(f"      ✅ C190 processados:      {count_c190_processados}")
        print(f"      ❌ C190 ignorados:        {count_c190_lidos - count_c190_processados}")
        print(f"      📋 Notas finais:          {len(resultado['notas'])}")
        print(f"      ✅ Notas com C170:        {notas_com_c170}")
        print(f"      ⚠️  Notas sem C170:        {notas_sem_c170}")
        print(f"      👤 Participantes:         {len(resultado['cabecalhos']['0150'])}")
        print(f"      🏷️  Produtos:              {len(resultado['cabecalhos']['0200'])}")