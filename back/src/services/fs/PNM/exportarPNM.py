from typing import Iterable, Dict, Any, List, Sequence, Optional
from collections import defaultdict
from sqlalchemy import text, bindparam
from .builderPNM import builderPNM

class ExportarPNM:
    def __init__(self, session, empresa_id: int, chunk_size: int = 5000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size = chunk_size

    @staticmethod
    def chunks(seq: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
        for i in range(0, len(seq), size):
            yield seq[i : i + size]

    def itens(self, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT DISTINCT
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
                c170.quant_bc_cofins AS quant_bc_cofins, c170.cod_cta AS cod_cta, c170.cod_nat AS cod_nat, 
                c100.cod_part AS fornecedor_cod_part,
                f.simples AS fornecedor_simples,
                f.decreto AS fornecedor_decreto
            FROM registro_c170 c170
            JOIN registro_c100 c100 
                ON c170.c100_id = c100.id
            JOIN fornecedores f 
                ON f.cod_part = c100.cod_part
                AND f.empresa_id = c170.empresa_id
            WHERE c170.empresa_id = :empresa_id
                AND c170.ativo = 1
                AND c100.ativo = 1
                -- AND c100.cod_mod IN ('01', '1B', '04', '55')
                AND c170.cfop IN ( '1101', '1401', '1102', '1403', '1910', '1116', '2101', '2102', '2401', '2403', '2910', '2116')
                AND ( (f.uf = 'CE' AND f.decreto = 0)OR f.uf != 'CE')
        """
        params = {"empresa_id": self.empresa_id}

        if c100_ids:
            c100_ids_unicos = list(set(c100_ids))
            query += " AND c170.c100_id IN :c100_ids"
            params["c100_ids"] = c100_ids_unicos
            
        query += " ORDER BY c170.c100_id, c170.id"
        
        if c100_ids:
            stmt = text(query).bindparams(bindparam("c100_ids", expanding=True))
        else:
            stmt = text(query)
        
        rows = self.session.execute(stmt, params).mappings().all()
        return list(rows)

    def cabecalhos(self, c100_ids: Sequence[int]) -> Dict[int, Dict[str, Any]]:
        if not c100_ids:
            return {}

        resultados: Dict[int, Dict[str, Any]] = {}
        base = text("""
            SELECT id AS c100_id, dt_doc, ind_emit, chv_nfe, vl_frt, vl_seg, vl_out_da
            FROM registro_c100
            WHERE id IN :ids AND ativo = 1
        """).bindparams(bindparam("ids", expanding=True))

        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size):
            rows = self.session.execute(base, {"ids": chunk}).mappings().all()
            for r in rows:
                resultados[r["c100_id"]] = dict(r)

        return resultados

    def produtos(self, cod_items: Sequence[str]) -> Dict[str, Dict[str, Any]]:
        if not cod_items:
            return {}

        resultados: Dict[str, Dict[str, Any]] = {}

        # dedupe e filtre None
        cods_unicos = list(set(filter(None, cod_items)))
        if not cods_unicos:
            return resultados

        # Se couber em um chunk, use um único chunk para reduzir round-trips
        effective_chunk = cods_unicos if len(cods_unicos) <= self.chunk_size else None

        # 1) Buscar dados do registro_0200 (metadados do produto) em batches
        q0200 = text("""
            SELECT cod_item, cod_ncm, cest
            FROM registro_0200
            WHERE empresa_id = :empresa_id AND cod_item IN :cods AND ativo = 1
        """).bindparams(bindparam("cods", expanding=True))

        map_0200: Dict[str, Dict[str, Any]] = {}
        if effective_chunk is not None:
            rows = self.session.execute(q0200, {"empresa_id": self.empresa_id, "cods": effective_chunk}).mappings().all()
            for r in rows:
                map_0200[r["cod_item"]] = dict(r)
        else:
            for chunk in self.chunks(cods_unicos, self.chunk_size):
                rows = self.session.execute(q0200, {"empresa_id": self.empresa_id, "cods": chunk}).mappings().all()
                for r in rows:
                    map_0200[r["cod_item"]] = dict(r)

        # 2) Buscar dados da tabela produtos (aliquota, etc.) em batches
        qprod = text("""
            SELECT codigo AS cod_item, aliquota AS aliquota_cadastro
            FROM produtos
            WHERE empresa_id = :empresa_id AND codigo IN :cods
        """).bindparams(bindparam("cods", expanding=True))

        map_prod: Dict[str, Dict[str, Any]] = {}
        if effective_chunk is not None:
            rows = self.session.execute(qprod, {"empresa_id": self.empresa_id, "cods": effective_chunk}).mappings().all()
            for r in rows:
                map_prod[r["cod_item"]] = dict(r)
        else:
            for chunk in self.chunks(cods_unicos, self.chunk_size):
                rows = self.session.execute(qprod, {"empresa_id": self.empresa_id, "cods": chunk}).mappings().all()
                for r in rows:
                    map_prod[r["cod_item"]] = dict(r)

        # 3) Mesclar resultados priorizando dados de registro_0200 quando presentes
        for cod in cods_unicos:
            r0200 = map_0200.get(cod)
            p = map_prod.get(cod)
            if not (r0200 or p):
                continue
            resultados[cod] = {
                "cod_item": cod,
                "cod_ncm": r0200.get("cod_ncm") if r0200 else None,
                "cod_cest": r0200.get("cest") if r0200 else None,
                "aliquota_cadastro": p.get("aliquota_cadastro") if p else None
            }

        return resultados

    def calculo_somas(self, c100_ids: Sequence[int]) -> Dict[int, float]:
        if not c100_ids:
            return {}
        resultado: Dict[int, float] = {}
        base = text("""
            SELECT c100_id, SUM(vl_item) AS soma_itens
            FROM registro_c170
            WHERE c100_id IN :ids AND ativo = 1
            GROUP BY c100_id
        """).bindparams(bindparam("ids", expanding=True))

        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size):
            rows = self.session.execute(base, {"ids": chunk}).mappings().all()
            for r in rows:
                resultado[r["c100_id"]] = float(r["soma_itens"] or 0.0)
        return resultado

    def gerar(self, c100_ids: Optional[Sequence[int]] = None) -> Dict[int, List[str]]:
        print(f"[DEBUG PNM] Iniciando com {len(c100_ids) if c100_ids else 'TODOS'} c100_ids")
        
        # 1. Buscar itens
        itens = self.itens(c100_ids)
        if not itens:
            return {}

        # 2. Extrair IDs únicos
        c100_ids_unicos = list({r["c100_id"] for r in itens if r.get("c100_id")})
        cod_items_unicos = list({r["cod_item"] for r in itens if r.get("cod_item")})

        # 3. Buscar cabeçalhos
        cabecalhos = self.cabecalhos(c100_ids_unicos)

        # 4. Buscar produtos
        dados_produtos = self.produtos(cod_items_unicos)

        # 5. Calcular somas
        somas = self.calculo_somas(c100_ids_unicos)

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