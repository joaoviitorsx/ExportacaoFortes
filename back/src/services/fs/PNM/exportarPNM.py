from typing import Iterable, Dict, Any, List, Sequence
from sqlalchemy import text, bindparam
from .builderPNM import builderPNM

class ExportarPNM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 1000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size

    @staticmethod
    def chunks(seq: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
        for i in range(0, len(seq), size):
            yield seq[i : i + size]

    #Busca os itens da C170 com todos os campos fiscais necessários.
    def itens(self) -> List[Dict[str, Any]]:
        q = text(
            """
            SELECT
                c170.id AS c170_id, c170.c100_id AS c100_id, c170.cod_item AS cod_item,
                c170.cfop AS cfop, c170.unid AS unid, c170.qtd AS qtd, c170.vl_item AS vl_item,
                c170.vl_desc AS vl_desc, c170.cst_icms AS cst_icms, c170.vl_bc_icms AS vl_bc_icms,
                c170.aliq_icms AS aliq_icms, c170.vl_icms AS vl_icms, c170.vl_bc_icms_st AS vl_bc_icms_st,
                c170.vl_icms_st AS vl_icms_st, c170.aliq_st AS aliq_st, c170.cst_ipi AS cst_ipi,
                c170.vl_bc_ipi AS vl_bc_ipi, c170.aliq_ipi AS aliq_ipi, c170.vl_ipi AS vl_ipi,
                c170.cst_pis AS cst_pis, c170.vl_bc_pis AS vl_bc_pis, c170.aliq_pis AS aliq_pis,
                c170.aliq_pis_reais AS aliq_pis_reais, c170.vl_pis AS vl_pis, c170.quant_bc_pis AS quant_bc_pis,
                c170.cst_cofins AS cst_cofins, c170.vl_bc_cofins AS vl_bc_cofins, c170.aliq_cofins AS aliq_cofins,
                c170.aliq_cofins_reais AS aliq_cofins_reais, c170.vl_cofins AS vl_cofins,
                c170.quant_bc_cofins AS quant_bc_cofins, c170.cod_cta AS cod_cta, c170.cod_nat AS cod_nat
            FROM registro_c170 c170
            JOIN registro_c100 c100 ON c170.c100_id = c100.id
            WHERE c170.empresa_id = :empresa_id AND c100.cod_mod IN ('01', '1B', '04', '55')
            ORDER BY c170.c100_id, c170.id
            """
        )
        rows = self.session.execute(q, {"empresa_id": self.empresa_id}).mappings().all()
        return list(rows)
    
    #Busca dados da C100 apenas para os IDs informados.
    def cabecalhos(self, c100_ids: Sequence[int]) -> Dict[int, Dict[str, Any]]:
        if not c100_ids: 
            return {}
        
        resultados: Dict[int, Dict[str, Any]] = {}
        base = text(
            "SELECT id AS c100_id, dt_doc, ind_emit, chv_nfe, vl_frt, vl_seg, vl_out_da FROM registro_c100 WHERE id IN :ids"
        ).bindparams(bindparam("ids", expanding=True))
        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size):
            rows = self.session.execute(base, {"ids": chunk}).mappings().all()
            for r in rows:
                resultados[r["c100_id"]] = dict(r)
        return resultados

    def produtos(self, cod_items: Sequence[str]) -> Dict[str, Dict[str, Any]]:
        if not cod_items: return {}
        
        resultados: Dict[str, Dict[str, Any]] = {}
        
        query = text(
            """
            SELECT 
                p.codigo AS cod_item,
                r.cod_ncm,
                r.cest AS cod_cest,
                p.aliquota AS aliquota_cadastro
            FROM produtos p
            LEFT JOIN registro_0200 r ON p.codigo = r.cod_item AND p.empresa_id = r.empresa_id
            WHERE p.empresa_id = :empresa_id AND p.codigo IN :cods
            """
        ).bindparams(bindparam("cods", expanding=True))

        cods_unicos = list(set(filter(None, cod_items)))
        for chunk in self.chunks(cods_unicos, self.chunk_size):
            params = {"empresa_id": self.empresa_id, "cods": chunk}
            rows = self.session.execute(query, params).mappings().all()
            for r in rows:
                resultados[r["cod_item"]] = dict(r)
        
        return resultados
    
    #Calcula a soma de vl_item por c100_id para o rateio.
    def calculo_somas(self, c100_ids: Sequence[int]) -> Dict[int, float]:
        if not c100_ids: 
            return {}
        resultado: Dict[int, float] = {}
        base = text(
            "SELECT c100_id, SUM(vl_item) AS soma_itens FROM registro_c170 WHERE c100_id IN :ids GROUP BY c100_id"
        ).bindparams(bindparam("ids", expanding=True))
        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size):
            rows = self.session.execute(base, {"ids": chunk}).mappings().all()
            for r in rows:
                resultado[r["c100_id"]] = float(r["soma_itens"] or 0.0)
        return resultado
    
    #Orquestra a busca e a geração das linhas PNM.
    def gerar(self) -> List[str]:
        itens = self.itens()
        if not itens: return []

        c100_ids = [r["c100_id"] for r in itens if r.get("c100_id")]
        cod_items = [r["cod_item"] for r in itens if r.get("cod_item")]

        cabecalhos = self.cabecalhos(c100_ids)
        dados_produtos = self.produtos(cod_items)
        somas = self.calculo_somas(c100_ids)

        linhas_pnm: List[str] = []
        for item_c170 in itens:
            c100_id = item_c170["c100_id"]
            head = cabecalhos.get(c100_id, {})
            prod = dados_produtos.get(item_c170.get("cod_item"), {})

            soma_itens_nota = somas.get(c100_id, 0.0)
            vl_item_atual = float(item_c170.get("vl_item") or 0.0)
            proporcao = (vl_item_atual / soma_itens_nota) if soma_itens_nota > 0 else 0.0

            dados_completos = {
                **item_c170,
                **head,
                **prod,
                "frete_rateado": round(float(head.get("vl_frt") or 0.0) * proporcao, 2),
                "seguro_rateado": round(float(head.get("vl_seg") or 0.0) * proporcao, 2),
                "outras_desp_rateado": round(float(head.get("vl_out_da") or 0.0) * proporcao, 2),
            }

            linha = builderPNM(dados_completos)
            linhas_pnm.append(linha)

        return linhas_pnm