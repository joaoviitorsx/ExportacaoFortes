from typing import Sequence, Dict, Any, List, Optional
from sqlalchemy import text, bindparam
from collections import defaultdict

class SnmRepository:
    def __init__(self, session):
        self.session = session

    def get_registros(self, empresa_id: int, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        # Etapa 1: Buscar dados dos itens (C170) com informações do cabeçalho (C100)
        itens = self.buscarItens(empresa_id, c100_ids)
        
        if not itens:
            return []
        
        # Etapa 2: Buscar totais por nota para fazer o rateio
        totais_por_nota = self.buscarTotais(empresa_id, c100_ids)
        
        # Etapa 3: Calcular rateio e agrupar por c100_id e alíquota
        registros_agrupados = self.calcular(itens, totais_por_nota)
        
        return registros_agrupados

    def buscarItens(self, empresa_id: int, c100_ids: Optional[Sequence[int]] = None) -> List[Dict[str, Any]]:
        """
        Busca TODOS os itens que podem gerar ST (mesmo critério do PNM):
        - Fornecedor CE sem decreto
        - Produto com alíquota válida (não ST, não ISENTO)
        """
        query = """
            SELECT
                c170.c100_id,
                c170.vl_item,
                c170.vl_desc,
                c170.vl_bc_icms,
                c170.vl_icms,
                c170.vl_ipi,
                c170.cst_icms,
                c170.cfop,
                c170.cod_item,
                CAST(COALESCE(p.aliquota, c170.aliq_icms) AS DECIMAL(10,2)) AS aliq_icms,
                c100.vl_frt,
                c100.vl_seg,
                c100.vl_out_da,
                e.simples AS empresa_simples,
                f.simples AS fornecedor_simples,
                f.decreto AS fornecedor_decreto,
                f.uf AS fornecedor_uf,
                p.aliquota AS aliquota_cadastro
            FROM registro_c170 AS c170
            JOIN registro_c100 AS c100
                ON c170.c100_id = c100.id
                AND c100.empresa_id = c170.empresa_id
                AND c100.ativo = 1
            INNER JOIN produtos AS p
                ON p.codigo = c170.cod_item
                AND p.empresa_id = c170.empresa_id
            INNER JOIN fornecedores AS f
                ON f.cod_part = c100.cod_part
                AND f.empresa_id = c170.empresa_id
            LEFT JOIN empresas AS e
                ON e.id = c100.empresa_id
            WHERE
                c170.empresa_id = :empresa_id
                AND c170.ativo = 1
                -- AND c100.cod_mod IN ('01', '1B', '04', '55')
                -- AND c170.cfop IN ('1101', '1401', '1102', '1403', '1910', '1116', '2101', '2102', '2401', '2403', '2910', '2116')
                AND p.aliquota IS NOT NULL 
                AND p.aliquota REGEXP '^[0-9]+\\.[0-9]*$|^[0-9]+$'
                AND CAST(p.aliquota AS DECIMAL(10,2)) > 0
                AND UPPER(TRIM(p.aliquota)) NOT IN ('ST', 'ISENTO')
                AND UPPER(TRIM(f.uf)) = 'CE'
                AND (f.decreto IS NULL OR TRIM(f.decreto) = '' OR TRIM(f.decreto) = 'False')
        """
        
        params = {"empresa_id": empresa_id}
        
        if c100_ids:
            query += " AND c100.id IN :c100_ids"
            params["c100_ids"] = list(set(c100_ids))
        
        if c100_ids:
            stmt = text(query).bindparams(bindparam("c100_ids", expanding=True))
        else:
            stmt = text(query)
        
        result = self.session.execute(stmt, params).mappings().all()
        return [dict(row) for row in result]

    #Calcula o valor total de cada nota (soma dos itens) para rateio
    def buscarTotais(self, empresa_id: int, c100_ids: Optional[Sequence[int]] = None) -> Dict[int, float]:
        query = """
            SELECT 
                c170.c100_id,
                SUM(c170.vl_item) AS vl_total
            FROM registro_c170 AS c170
            WHERE c170.empresa_id = :empresa_id
                AND c170.ativo = 1
        """
        
        params = {"empresa_id": empresa_id}
        
        if c100_ids:
            query += " AND c170.c100_id IN :c100_ids"
            params["c100_ids"] = list(set(c100_ids))
        
        query += " GROUP BY c170.c100_id"
        
        if c100_ids:
            stmt = text(query).bindparams(bindparam("c100_ids", expanding=True))
        else:
            stmt = text(query)
        
        result = self.session.execute(stmt, params).mappings().all()
        
        return {row["c100_id"]: float(row["vl_total"] or 0) for row in result}

    def calcular(self, itens: List[Dict[str, Any]], totais_por_nota: Dict[int, float]) -> List[Dict[str, Any]]:
        """
        Calcula o rateio e agrupa por c100_id + alíquota
        FILTRO: Apenas itens que atendem as condições de ST
        """
        grupos = defaultdict(lambda: {
            "c100_id": None,
            "aliq_icms": None,
            "vl_item": 0,
            "vl_desc": 0,
            "frete_rateado": 0,
            "seguro_rateado": 0,
            "outras_desp_rateado": 0,
            "vl_bc_icms": 0,
            "vl_icms": 0,
            "vl_ipi": 0,
            "cst_icms": None,
            "cfop": None,
            "empresa_simples": None,
            "fornecedor_simples": None,
            "fornecedor_decreto": None,
            "fornecedor_uf": None,
            "aliquota_cadastro": None
        })
        
        for item in itens:
            # Verificar se deve gerar ST (mesma lógica do PNM)
            fornecedor_uf = str(item.get("fornecedor_uf", "")).strip().upper()
            fornecedor_decreto = str(item.get("fornecedor_decreto", "")).strip()
            aliquota_cadastro = str(item.get("aliquota_cadastro", "")).strip().upper()
            
            # REGRA: Só gera SNM se passar nas mesmas condições do PNM campos 16-21
            if fornecedor_uf != "CE":
                continue
            
            if fornecedor_decreto == "True":
                continue
            
            if aliquota_cadastro in ("ST", "ISENTO", "", "None", "null"):
                continue
            
            # Se passou nas validações, agrupa
            c100_id = item["c100_id"]
            aliq_icms = float(item["aliq_icms"] or 0)
            chave = (c100_id, aliq_icms)
            
            vl_total_nota = totais_por_nota.get(c100_id, 0)
            vl_item = float(item["vl_item"] or 0)
            
            proporcao = (vl_item / vl_total_nota) if vl_total_nota > 0 else 0
            
            frete_rateado = proporcao * float(item["vl_frt"] or 0)
            seguro_rateado = proporcao * float(item["vl_seg"] or 0)
            outras_desp_rateado = proporcao * float(item["vl_out_da"] or 0)
            
            grupo = grupos[chave]
            grupo["c100_id"] = c100_id
            grupo["aliq_icms"] = aliq_icms
            grupo["vl_item"] += vl_item
            grupo["vl_desc"] += float(item["vl_desc"] or 0)
            grupo["frete_rateado"] += frete_rateado
            grupo["seguro_rateado"] += seguro_rateado
            grupo["outras_desp_rateado"] += outras_desp_rateado
            grupo["vl_bc_icms"] += float(item["vl_bc_icms"] or 0)
            grupo["vl_icms"] += float(item["vl_icms"] or 0)
            grupo["vl_ipi"] += float(item["vl_ipi"] or 0)
            
            grupo["cst_icms"] = item["cst_icms"]
            grupo["cfop"] = item["cfop"]
            grupo["empresa_simples"] = item["empresa_simples"]
            grupo["fornecedor_simples"] = item["fornecedor_simples"]
            grupo["fornecedor_decreto"] = item["fornecedor_decreto"]
            grupo["fornecedor_uf"] = item["fornecedor_uf"]
            grupo["aliquota_cadastro"] = item["aliquota_cadastro"]
        
        resultado = sorted(grupos.values(), key=lambda x: (x["c100_id"], x["aliq_icms"]))
        
        return resultado