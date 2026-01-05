from typing import Sequence, Dict, Any, List, Optional, Iterable
from sqlalchemy import text, bindparam

class PnmRepository:
    def __init__(self, session, chunk_size: int = 5000):
        self.session = session
        self.chunk_size = chunk_size

    @staticmethod
    def chunks(seq: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
        for i in range(0, len(seq), size):
            yield seq[i : i + size]

    def get_itens(self, empresa_id: int, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        query = """
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
                c170.quant_bc_cofins AS quant_bc_cofins, c170.cod_cta AS cod_cta, c170.cod_nat AS cod_nat, 
                c100.cod_part AS fornecedor_cod_part,
                f.simples AS fornecedor_simples,
                f.decreto AS fornecedor_decreto,
                f.uf AS fornecedor_uf
            FROM registro_c170 c170
            JOIN registro_c100 c100 
                ON c170.c100_id = c100.id
            LEFT JOIN fornecedores f 
                ON f.cod_part = c100.cod_part
                AND f.empresa_id = c170.empresa_id
            WHERE c170.empresa_id = :empresa_id
                AND c170.ativo = 1
                AND c100.ativo = 1
                -- AND c100.cod_mod IN ('01', '1B', '04', '55')
                -- AND c170.cfop IN ('1101', '1401', '1102', '1403', '1910', '1116', '2101', '2102', '2401', '2403', '2910', '2116')
        """
        params = {"empresa_id": empresa_id}

        if c100_ids:
            c100_ids_unicos = list(set(c100_ids))
            query += " AND c170.c100_id IN :c100_ids"
            params["c100_ids"] = c100_ids_unicos
        
        query += " ORDER BY c170.c100_id, c170.id"
        
        if c100_ids:
            stmt = text(query).bindparams(bindparam("c100_ids", expanding=True))
        else:
            stmt = text(query)
        
        result = self.session.execute(stmt, params).mappings().all()
        return [dict(row) for row in result]

    def get_cabecalhos(self, c100_ids: Sequence[int]) -> Dict[int, Dict[str, Any]]:
        if not c100_ids:
            return {}

        resultados: Dict[int, Dict[str, Any]] = {}
        query = text("""
            SELECT id AS c100_id, dt_doc, ind_emit, chv_nfe, vl_frt, vl_seg, vl_out_da
            FROM registro_c100
            WHERE id IN :ids AND ativo = 1
        """).bindparams(bindparam("ids", expanding=True))

        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size):
            rows = self.session.execute(query, {"ids": chunk}).mappings().all()
            for r in rows:
                resultados[r["c100_id"]] = dict(r)

        return resultados

    def get_produtos(self, empresa_id: int, cod_items: Sequence[str]) -> Dict[str, Dict[str, Any]]:
        if not cod_items:
            return {}

        # Dedupe e filtre None
        cods_unicos = list(set(filter(None, cod_items)))
        if not cods_unicos:
            return {}

        # NOVO: Buscar matriz_id para usar na busca de produtos
        # Se empresa for filial, busca produtos da matriz; senão, busca próprios
        empresa_query = text("""
            SELECT matriz_id FROM empresas WHERE id = :empresa_id
        """)
        empresa_result = self.session.execute(empresa_query, {"empresa_id": empresa_id}).first()
        
        # Se tem matriz_id diferente do próprio id, usar matriz_id; senão, usar próprio id
        empresa_id_produtos = empresa_result[0] if empresa_result and empresa_result[0] and empresa_result[0] != empresa_id else empresa_id
        
        print(f"[DEBUG PNM] Buscando produtos: empresa_id={empresa_id}, matriz_id={empresa_id_produtos}")

        # Queries
        q0200 = text("""
            SELECT cod_item, descr_item, cod_barra, unid_inv, cod_ncm, 
                   SUBSTRING(cod_ncm, 1, 2) AS cod_gen, 
                   cest
            FROM registro_0200
            WHERE empresa_id = :empresa_id AND cod_item IN :cods AND ativo = 1
        """).bindparams(bindparam("cods", expanding=True))

        qprod = text("""
            SELECT codigo AS cod_item, aliquota AS aliquota_cadastro
            FROM produtos
            WHERE empresa_id = :empresa_id AND codigo IN :cods
        """).bindparams(bindparam("cods", expanding=True))

        # Buscar em chunks
        map_0200: Dict[str, Dict[str, Any]] = {}
        map_prod: Dict[str, Dict[str, Any]] = {}

        for chunk in self.chunks(cods_unicos, self.chunk_size):
            # Buscar registro_0200 (sempre usa empresa_id original - dados da nota)
            rows_0200 = self.session.execute(q0200, {"empresa_id": empresa_id, "cods": chunk}).mappings().all()
            for r in rows_0200:
                map_0200[r["cod_item"]] = dict(r)

            # Buscar produtos (usa empresa_id_produtos - pode ser da matriz)
            rows_prod = self.session.execute(qprod, {"empresa_id": empresa_id_produtos, "cods": chunk}).mappings().all()
            for r in rows_prod:
                map_prod[r["cod_item"]] = dict(r)

        # Mesclar resultados
        resultados = {}
        for cod in cods_unicos:
            r0200 = map_0200.get(cod, {})
            p = map_prod.get(cod, {})
            
            resultados[cod] = {
                "cod_item": cod,
                "descr_item": r0200.get("descr_item", ""),
                "cod_barra": r0200.get("cod_barra", ""),
                "unid_inv": r0200.get("unid_inv", "UN"),
                "cod_ncm": r0200.get("cod_ncm", ""),
                "cod_gen": r0200.get("cod_gen", ""),
                "cod_cest": r0200.get("cest", ""),
                "aliquota_cadastro": p.get("aliquota_cadastro")
            }

        return resultados

    def get_somas_itens(self, c100_ids: Sequence[int]) -> Dict[int, float]:
        if not c100_ids:
            return {}

        resultado: Dict[int, float] = {}
        query = text("""
            SELECT c100_id, SUM(vl_item) AS soma_itens
            FROM registro_c170
            WHERE c100_id IN :ids AND ativo = 1
            GROUP BY c100_id
        """).bindparams(bindparam("ids", expanding=True))

        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size):
            rows = self.session.execute(query, {"ids": chunk}).mappings().all()
            for r in rows:
                resultado[r["c100_id"]] = float(r["soma_itens"] or 0.0)

        return resultado