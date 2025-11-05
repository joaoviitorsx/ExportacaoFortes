from typing import Dict, Any, List, Optional, Sequence
from collections import defaultdict
from .builderSNM import builderSNM
from ....repositories.camposRepo.snm_repository import SnmRepository

class ExportarSNM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 5000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size
        self.repo = SnmRepository(session)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> Dict[int, List[str]]:
        registros = self.repo.get_registros(self.empresa_id, c100_ids)
        
        if not registros:
            return {}

        snm_map: Dict[int, List[str]] = defaultdict(list)
        
        for registro in registros:
            c100_id = registro["c100_id"]
            
            fornecedor_uf = str(registro.get("fornecedor_uf", "")).strip().upper()
            fornecedor_decreto = registro.get("fornecedor_decreto")
            
            # Normalizar decreto para boolean
            if isinstance(fornecedor_decreto, bool):
                decreto_bool = fornecedor_decreto
            elif isinstance(fornecedor_decreto, str):
                decreto_bool = fornecedor_decreto.lower() in ["true", "1"]
            elif isinstance(fornecedor_decreto, int):
                decreto_bool = fornecedor_decreto == 1
            else:
                decreto_bool = False
            
            # Se for CE com decreto, pular este registro
            if fornecedor_uf == "CE" and decreto_bool:
                continue
            
            linha = builderSNM(registro)
            snm_map[c100_id].append(linha)

        return dict(snm_map)

    def gerarNota(self, c100_id: int) -> List[str]:
        snm_dict = self.gerar([c100_id])
        return snm_dict.get(c100_id, [])