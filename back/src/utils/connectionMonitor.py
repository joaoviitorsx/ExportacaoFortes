import asyncio
from sqlalchemy.exc import OperationalError
from typing import Callable, Optional


class ConnectionMonitor:
    def __init__(self, retry_interval: int = 3):

        self.retry_interval = retry_interval
        self.is_monitoring = False
        self.callbacks = []
    
    async def check_connection(self, test_function: Callable) -> bool:
        try:
            result = test_function()
            # Se a função de teste retorna True/False diretamente, usar isso
            if isinstance(result, bool):
                return result
            # Se retornou dict com erro, não está conectado
            if isinstance(result, dict) and "erro" in result:
                return False
            # Se retornou algo válido (não None, não erro), está conectado
            if result is not None:
                return True
            return False
        except OperationalError:
            return False
        except Exception as e:
            print(f"[DEBUG] Erro ao testar conexão: {e}")
            return False
    
    async def monitor_and_retry( self, test_function: Callable, on_connected: Optional[Callable] = None, on_retry: Optional[Callable[[int], None]] = None ):
        self.is_monitoring = True
        attempt = 0
        
        print("[DEBUG] Iniciando monitoramento de conexão...")
        
        while self.is_monitoring:
            attempt += 1
            
            print(f"[DEBUG] Tentativa {attempt} de reconexão...")
            
            if on_retry:
                try:
                    on_retry(attempt)
                except Exception as e:
                    print(f"[DEBUG] Erro ao chamar on_retry: {e}")
            
            is_connected = await self.check_connection(test_function)
            
            print(f"[DEBUG] Resultado da tentativa {attempt}: {'CONECTADO' if is_connected else 'FALHOU'}")
            
            if is_connected:
                print("[DEBUG] Conexão restabelecida! Chamando callback...")
                if on_connected:
                    try:
                        on_connected()
                    except Exception as e:
                        print(f"[DEBUG] Erro ao chamar on_connected: {e}")
                self.is_monitoring = False
                print("[DEBUG] Monitoramento finalizado.")
                break
            
            print(f"[DEBUG] Aguardando {self.retry_interval} segundos antes da próxima tentativa...")
            await asyncio.sleep(self.retry_interval)
    
    def stop_monitoring(self):
        self.is_monitoring = False

_connection_monitor = ConnectionMonitor(retry_interval=3)


def get_connection_monitor() -> ConnectionMonitor:
    return _connection_monitor
