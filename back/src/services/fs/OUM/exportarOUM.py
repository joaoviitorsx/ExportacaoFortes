from typing import List, Dict
from .builderOUM import builderOUM

class ExportarOUM:
    def __init__(self, session):
        self.session = session

    def gerar(self, produtos: List[Dict]) -> Dict[str, List[str]]:
        oum_map = {}
        
        for produto in produtos:
            cod_item = produto.get("cod_item")
            unid_inv = produto.get("unid_inv")
            
            # Só gera OUM se tiver código e unidade
            if not cod_item or not unid_inv:
                continue
            
            linha_oum = builderOUM(produto)
            
            if cod_item not in oum_map:
                oum_map[cod_item] = []
            
            oum_map[cod_item].append(linha_oum)
        
        return oum_map