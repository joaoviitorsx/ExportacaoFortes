import queue
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import time

from ....src.services.etl.leitorService import LeitorService
from ....src.services.etl.persistenciaService import Persistencia
from ....src.services.etl.softDeleteService import SoftDeleteService
from ....src.config.db.conexaoFS import getSessionFS

class PipelineService:
    def __init__(self, session, empresa_id, arquivos: list[str], num_workers=None, buffer_size=50000):
        self.session = session
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        
        # Otimização: ajustar workers baseado em CPU/IO
        if num_workers is None:
            # CPU cores * 2 é bom para operações IO-bound
            num_workers = min(multiprocessing.cpu_count() * 2, len(arquivos) * 2)
        
        self.num_workers = max(2, num_workers)  # Mínimo de 2 workers
        self.buffer_size = buffer_size  # Aumentado para 50k

        # Usar Queue com limite para evitar consumir muita memória
        self.fila = queue.PriorityQueue(maxsize=buffer_size * 2)
        self.threads_leitura = []
        self.threads_workers = []
        
        # Controle de estatísticas
        self.stats = {
            'registros_processados': 0,
            'tempo_inicio': None,
            'tempo_fim': None
        }

    def executar(self):
        self.stats['tempo_inicio'] = time.time()
        print(f"[INFO] Iniciando pipeline otimizado:")
        print(f"  - Arquivos: {len(self.arquivos)}")
        print(f"  - Workers: {self.num_workers}")
        print(f"  - Buffer size: {self.buffer_size}")
        
        periodo = SoftDeleteService.extrairPeriodo(self.arquivos)
        SoftDeleteService.softDelete(self.session, self.empresa_id, periodo)

        # Criar workers de persistência com ThreadPoolExecutor para melhor gerenciamento
        workers = []
        for i in range(self.num_workers):
            workerSession = getSessionFS()
            worker = Persistencia(self.fila, workerSession, self.empresa_id)
            worker.name = f"Worker-{i+1}"
            worker.start()
            workers.append(worker)

        try:
            # Criar threads de leitura com ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=len(self.arquivos)) as executor:
                futures = []
                
                for idx, arquivo in enumerate(self.arquivos):
                    leitor = LeitorService(
                        self.session,
                        self.empresa_id,
                        [arquivo],
                        self.fila,
                        self.buffer_size
                    )
                    future = executor.submit(leitor.executar)
                    futures.append(future)
                
                # Aguardar término de todas as leituras
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        print(f"[ERRO] Falha na leitura: {e}")

            print("[INFO] Todas as leituras finalizadas. Aguardando processamento...")
            
            # Aguardar fila esvaziar
            self.fila.join()
            print("[INFO] Fila de processamento vazia.")

        except Exception as e:
            print(f"[ERRO] Falha no pipeline: {e}")
            raise
        
        finally:
            # Enviar sinal de parada para todos os workers
            print("[INFO] Enviando sinal de parada para workers...")
            for _ in workers:
                self.fila.put((float("inf"), "parou", None, None))

            # Aguardar finalização dos workers com timeout
            for w in workers:
                w.join(timeout=30)
                if w.is_alive():
                    print(f"[WARN] Worker {w.name} não finalizou no timeout")

            self.stats['tempo_fim'] = time.time()
            self._exibir_estatisticas()

    def _exibir_estatisticas(self):
        """Exibe estatísticas do processamento"""
        tempo_total = self.stats['tempo_fim'] - self.stats['tempo_inicio']
        print("\n" + "="*60)
        print("ESTATÍSTICAS DO PIPELINE")
        print("="*60)
        print(f"Tempo total: {tempo_total:.2f}s")
        print(f"Arquivos processados: {len(self.arquivos)}")
        print(f"Workers utilizados: {self.num_workers}")
        print(f"Taxa média: {len(self.arquivos)/tempo_total:.2f} arquivos/s")
        print("="*60 + "\n")