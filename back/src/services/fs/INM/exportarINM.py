from collections import defaultdict
from typing import Dict, Any, List, Optional, Sequence
from .builderINM import builderINM
from ....repositories.camposRepo.inm_repository import InmRepository

class ExportarINM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 1000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size
        self.repo = InmRepository(session)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> Dict[int, List[str]]:
        registros = self.repo.get_registros(self.empresa_id, c100_ids)
        
        if not registros:
            return {}

        inm_map: Dict[int, List[str]] = defaultdict(list)
        
        for registro in registros:
            c100_id = registro["c100_id"]
            linha = builderINM(registro)
            inm_map[c100_id].append(linha)

        return dict(inm_map)

    def gerarNota(self, c100_id: int) -> List[str]:
        inm_dict = self.gerar([c100_id])
        return inm_dict.get(c100_id, [])