from typing import List
from .builderNFM import builderNFM
from ..PNM.exportarPNM import ExportarPNM
from ..INM.exportarINM import ExportarINM
from ..SNM.exportarSNM import ExportarSNM
from ....repositories.camposRepo.nfm_repository import NFMRepository

class ExportarNFM:
    def __init__(self, session, empresa_id: int):
        self.session = session
        self.empresa_id = empresa_id
        self.repo = NFMRepository(session)

        self.exportar_pnm = ExportarPNM(session, empresa_id)
        self.exportar_inm = ExportarINM(session, empresa_id)
        self.exportar_snm = ExportarSNM(session, empresa_id)

    def gerar(self) -> List[str]:
        documentos = self.repo.get_notas(self.empresa_id)
        
        if not documentos:
            return []

        c100_ids = [doc["c100_id"] for doc in documentos]
        print(f"[DEBUG NFM] Total de c100_ids: {len(c100_ids)}")

        # Buscar dados relacionados de PNM, INM e SNM
        pnm_map = self.exportar_pnm.gerar(c100_ids)
        inm_map = self.exportar_inm.gerar(c100_ids)
        snm_map = self.exportar_snm.gerar(c100_ids)

        # Montagem final
        linhas_nfm: List[str] = []

        for dados_doc in documentos:
            c100_id = dados_doc["c100_id"]

            # Só adiciona NFM se existir pelo menos um PNM
            if c100_id not in pnm_map:
                continue
            
            # Adiciona linha NFM (cabeçalho)
            linha_nfm = builderNFM(dados_doc)
            linhas_nfm.append(linha_nfm)

            # Adiciona linhas PNM (itens)
            if pnm_map.get(c100_id):
                linhas_nfm.extend(pnm_map[c100_id])
            
            # Adiciona linhas INM (totalizadores)
            if inm_map.get(c100_id):
                linhas_nfm.extend(inm_map[c100_id])
            
            # Adiciona linhas SNM (sumarização por alíquota)
            if snm_map.get(c100_id):
                linhas_nfm.extend(snm_map[c100_id])
        
        return linhas_nfm