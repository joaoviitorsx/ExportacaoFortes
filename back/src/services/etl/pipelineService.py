import threading
import queue

from src.services.etl.leitorService import LeitorService
from src.services.etl.persistenciaService import Persistencia

from src.config.db.conexaoFS import getSessionFS

class PipelineService:
    def __init__(self, session, empresa_id, arquivos: list[str], num_workers=2, buffer_size=5000):
        self.session = session
        self.empresa_id = empresa_id
        self.arquivos = arquivos
        self.num_workers = num_workers
        self.buffer_size = buffer_size

        self.fila = queue.PriorityQueue()
        self.threads_leitura = []
        self.threads_workers = []

    def executar(self):
        print(f"[INFO] Iniciando pipeline para {len(self.arquivos)} arquivo(s).")

        # 1. Criar workers de persistência (consumidores)
        for _ in range(self.num_workers):
            workerSession = getSessionFS()
            worker = Persistencia(self.fila, workerSession, self.empresa_id)
            worker.start()
            self.threads_workers.append(worker)

        try:
            # 2. Criar threads de leitura (produtores)
            for arquivo in self.arquivos:
                leitor = LeitorService(
                    self.session,
                    self.empresa_id,
                    [arquivo],
                    self.fila,
                    self.buffer_size
                )
                t = threading.Thread(target=leitor.executar)
                t.start()
                self.threads_leitura.append(t)

            # 3. Aguardar término da leitura
            for t in self.threads_leitura:
                t.join()
            print("[INFO] Pipeline de leituras encerrado.")
            self.fila.join()

        finally:
            for _ in self.threads_workers:
                self.fila.put((float("inf"), "parou", None, None))

            for w in self.threads_workers:
                w.join()

            print("[INFO] Pipeline finalizado com sucesso.")
