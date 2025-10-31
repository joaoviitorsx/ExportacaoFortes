from typing import List, Dict, Any
from ...repositories.registrosRepo.registro0000Repository import Registro0000Repository
from ...repositories.registrosRepo.registro0150Repository import Registro0150Repository
from ...repositories.registrosRepo.registro0200Repository import Registro0200Repository
from ...repositories.registrosRepo.registroC100Repository import RegistroC100Repository
from ...repositories.registrosRepo.registroC170Repository import RegistroC170Repository
from ...repositories.registrosRepo.registroC190Repository import RegistroC190Repository


class PersistenciaService:
    """
    Serviço de persistência linear - processa arquivos de forma síncrona.
    Garante integridade referencial entre C100, C170 e C190.
    """

    def __init__(self, session):
        self.session = session
        
        # Repositories
        self.repo0000 = Registro0000Repository(session)
        self.repo0150 = Registro0150Repository(session)
        self.repo0200 = Registro0200Repository(session)
        self.repoC100 = RegistroC100Repository(session)
        self.repoC170 = RegistroC170Repository(session)
        self.repoC190 = RegistroC190Repository(session)

    def salvar_arquivo(self, dados: Dict[str, Any]) -> Dict[str, int]:
        """
        Salva todos os dados de um arquivo SPED.
        
        Ordem de salvamento:
        1. Cabeçalhos (0000, 0150, 0200)
        2. Notas fiscais (C100 + C170 + C190) em lote
        
        Args:
            dados: Estrutura retornada pelo LeitorService.ler_arquivo()
        
        Returns:
            Estatísticas de salvamento
        """
        stats = {
            "0000": 0,
            "0150": 0,
            "0200": 0,
            "c100": 0,
            "c170": 0,
            "c190": 0,
            "notas_ignoradas": 0
        }

        try:
            # ============================================
            # 1. SALVAR CABEÇALHOS
            # ============================================
            print("\n💾 Salvando cabeçalhos...")
            
            if dados["cabecalhos"]["0000"]:
                self.repo0000.salvamento(dados["cabecalhos"]["0000"])
                stats["0000"] = len(dados["cabecalhos"]["0000"])
                self.session.commit()
            
            if dados["cabecalhos"]["0150"]:
                self.repo0150.salvamento(dados["cabecalhos"]["0150"])
                stats["0150"] = len(dados["cabecalhos"]["0150"])
                self.session.commit()
            
            if dados["cabecalhos"]["0200"]:
                self.repo0200.salvamento(dados["cabecalhos"]["0200"])
                stats["0200"] = len(dados["cabecalhos"]["0200"])
                self.session.commit()
            
            print(f"   ✅ Cabeçalhos salvos: 0000={stats['0000']}, "
                  f"0150={stats['0150']}, 0200={stats['0200']}")

            # ============================================
            # 2. SALVAR NOTAS EM LOTE
            # ============================================
            print("\n💾 Salvando notas fiscais...")
            
            lote_c100 = []
            lote_c170 = []
            lote_c190 = []

            for nota in dados["notas"]:
                # Ignorar notas sem itens
                if not nota["c170"]:
                    stats["notas_ignoradas"] += 1
                    continue
                
                # Preparar C100
                c100 = nota["c100"]
                doc_key = c100["doc_key"]
                lote_c100.append(c100)
                
                # *** CORREÇÃO: Não adicionar _doc_key_temp, manter doc_key original ***
                # C170 já tem doc_key adicionado no leitorService.py linha 189
                for c170 in nota["c170"]:
                    lote_c170.append(c170)
                
                # C190 já tem doc_key adicionado no leitorService.py linha 217
                for c190 in nota["c190"]:
                    lote_c190.append(c190)

            # Salvar C100 e obter IDs gerados
            if lote_c100:
                print(f"   📄 Salvando {len(lote_c100)} registros C100...")
                self.repoC100.salvamento(lote_c100)
                self.session.commit()
                stats["c100"] = len(lote_c100)
                
                # Buscar IDs dos C100 recém-inseridos
                periodo = lote_c100[0]["periodo"]
                empresa_id = lote_c100[0]["empresa_id"]
                rows = self.repoC100.buscarIDS(periodo, empresa_id)
                
                if not rows:
                    print(f"   ⚠️  AVISO: buscarIDS() não retornou nenhum registro")
                    return stats
                
                # Criar mapa: doc_key -> id_c100
                mapa_ids = {}
                for row in rows:
                    try:
                        # Tentar como dict primeiro
                        if isinstance(row, dict):
                            doc_key_db = row["doc_key"]
                            id_c100 = row["id"]
                        # Tentar como tuple/list
                        elif isinstance(row, (tuple, list)):
                            id_c100 = row[0]
                            doc_key_db = row[1]
                        # Tentar como objeto com atributos (SQLAlchemy Row)
                        else:
                            id_c100 = getattr(row, 'id', None) or row[0]
                            doc_key_db = getattr(row, 'doc_key', None) or row[1]
                        
                        if doc_key_db and id_c100:
                            mapa_ids[doc_key_db] = id_c100
                        else:
                            print(f"   ⚠️  Row inválido: {row}")
                            
                    except Exception as e:
                        print(f"   ⚠️  Erro ao processar row: {row} - {e}")
                        continue
                
                print(f"   ✅ C100 salvos: {stats['c100']} (IDs mapeados: {len(mapa_ids)})")
                
                # Debug: mostrar alguns mapeamentos
                if mapa_ids:
                    sample = list(mapa_ids.items())[:3]
                    for doc_key_sample, id_sample in sample:
                        print(f"      Exemplo: doc_key={doc_key_sample[:50]}... -> id={id_sample}")
                
                # *** CORREÇÃO: Adicionar c100_id SEM remover doc_key ***
                c170_sem_id = 0
                for c170 in lote_c170:
                    # doc_key já existe no objeto (adicionado no leitorService)
                    doc_key = c170.get("doc_key")
                    
                    if not doc_key:
                        c170_sem_id += 1
                        if c170_sem_id <= 3:
                            print(f"   ⚠️  C170 sem doc_key: {c170}")
                        continue
                    
                    # Adicionar c100_id baseado no doc_key
                    c170["c100_id"] = mapa_ids.get(doc_key)
                    
                    if not c170["c100_id"]:
                        c170_sem_id += 1
                        if c170_sem_id <= 3:
                            print(f"   ⚠️  C170 sem c100_id para doc_key={doc_key[:50]}...")
                
                if c170_sem_id > 0:
                    print(f"   ⚠️  Total de C170 sem c100_id: {c170_sem_id}")
                
                # Salvar C170
                lote_c170_validos = [c for c in lote_c170 if c.get("c100_id")]
                if lote_c170_validos:
                    print(f"   📦 Salvando {len(lote_c170_validos)} registros C170...")
                    self.repoC170.salvamento(lote_c170_validos)
                    self.session.commit()
                    stats["c170"] = len(lote_c170_validos)
                    print(f"   ✅ C170 salvos: {stats['c170']}")
                else:
                    print(f"   ⚠️  Nenhum C170 válido para salvar!")
                
                # *** CORREÇÃO: Adicionar c100_id SEM remover doc_key ***
                c190_sem_id = 0
                for c190 in lote_c190:
                    # doc_key já existe no objeto (adicionado no leitorService)
                    doc_key = c190.get("doc_key")
                    
                    if not doc_key:
                        c190_sem_id += 1
                        if c190_sem_id <= 3:
                            print(f"   ⚠️  C190 sem doc_key: {c190}")
                        continue
                    
                    # Adicionar c100_id baseado no doc_key
                    c190["c100_id"] = mapa_ids.get(doc_key)
                    
                    if not c190["c100_id"]:
                        c190_sem_id += 1
                        if c190_sem_id <= 3:
                            print(f"   ⚠️  C190 sem c100_id para doc_key={doc_key[:50]}...")
                
                if c190_sem_id > 0:
                    print(f"   ⚠️  Total de C190 sem c100_id: {c190_sem_id}")
                
                # Salvar C190
                lote_c190_validos = [c for c in lote_c190 if c.get("c100_id")]
                if lote_c190_validos:
                    print(f"   📊 Salvando {len(lote_c190_validos)} registros C190...")
                    self.repoC190.salvamento(lote_c190_validos)
                    self.session.commit()
                    stats["c190"] = len(lote_c190_validos)
                    print(f"   ✅ C190 salvos: {stats['c190']}")
                else:
                    print(f"   ⚠️  Nenhum C190 válido para salvar!")
            
            print(f"\n📊 Resumo: {stats['c100']} notas, {stats['c170']} itens, "
                  f"{stats['c190']} totalizadores, {stats['notas_ignoradas']} ignoradas")
            
            return stats

        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")
            import traceback
            traceback.print_exc()
            self.session.rollback()
            raise