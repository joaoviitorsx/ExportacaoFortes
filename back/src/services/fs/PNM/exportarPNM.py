from typing import Dict, Any, List, Sequence, Optional
from collections import defaultdict
from .builderPNM import builderPNM
from ....repositories.camposRepo.pnm_repository import PnmRepository

class ExportarPNM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 5000):
        self.session = session
        self.empresa_id = empresa_id
        self.repo = PnmRepository(session, chunk_size)

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> Dict[int, List[str]]:
        print(f"[DEBUG PNM] Iniciando com {len(c100_ids) if c100_ids else 'TODOS'} c100_ids")
        
        # 1. Buscar itens usando o repositório
        itens = self.repo.get_itens(self.empresa_id, c100_ids)
        if not itens:
            return {}

        # 2. Extrair IDs únicos
        c100_ids_unicos = list({r["c100_id"] for r in itens if r.get("c100_id")})
        cod_items_unicos = list({r["cod_item"] for r in itens if r.get("cod_item")})

        # 3. Buscar cabeçalhos usando o repositório
        cabecalhos = self.repo.get_cabecalhos(c100_ids_unicos)

        # 4. Buscar produtos usando o repositório
        dados_produtos = self.repo.get_produtos(self.empresa_id, cod_items_unicos)

        # 5. Calcular somas usando o repositório
        somas = self.repo.get_somas_itens(c100_ids_unicos)

        # 6. Montar linhas PNM
        pnm_map: Dict[int, List[str]] = defaultdict(list)
        
        for item_c170 in itens:
            c100_id = item_c170["c100_id"]
            head = cabecalhos.get(c100_id, {})
            prod = dados_produtos.get(item_c170.get("cod_item"), {})

            soma_itens_nota = somas.get(c100_id, 0.0)
            vl_item_atual = float(item_c170.get("vl_item") or 0.0)
            proporcao = (vl_item_atual / soma_itens_nota) if soma_itens_nota > 0 else 0.0

            dados = {
                **item_c170,
                **head,
                **prod,
                "frete_rateado": round(float(head.get("vl_frt") or 0.0) * proporcao, 2),
                "seguro_rateado": round(float(head.get("vl_seg") or 0.0) * proporcao, 2),
                "outras_desp_rateado": round(float(head.get("vl_out_da") or 0.0) * proporcao, 2),
            }

            linha = builderPNM(dados)
            pnm_map[c100_id].append(linha)
        
        return dict(pnm_map)
    
    def geradorNota(self, c100_id: int) -> List[str]:
        pnm_dict = self.gerar([c100_id])
        return pnm_dict.get(c100_id, [])