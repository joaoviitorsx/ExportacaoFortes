from typing import Iterable, Dict, Any, List, Sequence
from sqlalchemy import text, bindparam
from src.services.fs.PNM.builderPNM import builderPNM


class ExportarPNM:
    """
    Exporta os registros PNM (Produtos da Nota Fiscal de Mercadorias) em etapas,
    melhorando legibilidade e testabilidade sem perder performance.

    Etapas:
      1) Buscar itens (C170)
      2) Buscar cabeçalhos (C100) apenas para os c100_id coletados
      3) Buscar produtos (0200) apenas para os cod_item coletados
      4) Buscar soma de itens por nota (para rateio)
      5) Montar linhas via builderPNM
    """

    def __init__(self, session, empresa_id: int, chunk_size_in: int = 1000):
        self.session = session
        self.empresa_id = empresa_id
        self.chunk_size_in = chunk_size_in  # controla tamanho do IN (...) para DBs que limitam params

    # =========================
    # Helpers internos
    # =========================
    @staticmethod
    def chunks(seq: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
        for i in range(0, len(seq), size):
            yield seq[i : i + size]

    # =========================
    # 1) Itens (C170)
    # =========================
    def itens(self) -> List[Dict[str, Any]]:
        """
        Busca os itens C170 com os campos necessários, incluindo c100_id.
        Filtra por empresa e modelos de documento válidos.
        """
        q = text(
            """
            SELECT
                c170.id               AS c170_id,
                c170.c100_id          AS c100_id,
                c170.cod_item         AS cod_item,
                c170.cfop             AS cfop,
                c170.unid             AS unid,
                c170.qtd              AS qtd,
                c170.vl_item          AS vl_item,
                c170.vl_desc          AS vl_desc,
                c170.cst_icms         AS cst_icms,
                c170.vl_bc_icms       AS vl_bc_icms,
                c170.aliq_icms        AS aliq_icms,
                c170.vl_icms          AS vl_icms,
                c170.vl_bc_icms_st    AS vl_bc_icms_st,
                c170.vl_icms_st       AS vl_icms_st,
                c170.aliq_st          AS aliq_st,
                c170.cst_ipi          AS cst_ipi,
                c170.vl_bc_ipi        AS vl_bc_ipi,
                c170.aliq_ipi         AS aliq_ipi,
                c170.vl_ipi           AS vl_ipi,
                c170.cst_pis          AS cst_pis,
                c170.vl_bc_pis        AS vl_bc_pis,
                c170.aliq_pis         AS aliq_pis,
                c170.aliq_pis_reais   AS aliq_pis_reais,
                c170.vl_pis           AS vl_pis,
                c170.quant_bc_pis     AS quant_bc_pis,
                c170.cst_cofins       AS cst_cofins,
                c170.vl_bc_cofins     AS vl_bc_cofins,
                c170.aliq_cofins      AS aliq_cofins,
                c170.aliq_cofins_reais AS aliq_cofins_reais,
                c170.vl_cofins        AS vl_cofins,
                c170.quant_bc_cofins  AS quant_bc_cofins,
                c170.cod_cta          AS cod_cta,
                c170.cod_nat          AS cod_nat
            FROM registro_c170 c170
            JOIN registro_c100 c100
              ON c170.c100_id = c100.id
            WHERE c170.empresa_id = :empresa_id
              AND c100.cod_mod IN ('01', '1B', '04', '55')
            ORDER BY c170.c100_id, c170.id
            """
        )
        rows = self.session.execute(q, {"empresa_id": self.empresa_id}).mappings().all()
        return list(rows)

    # =========================
    # 2) Cabeçalhos (C100)
    # =========================
    def cabecalhos(self, c100_ids: Sequence[int]) -> Dict[int, Dict[str, Any]]:
        """
        Busca dados do C100 (cabeçalho) apenas para os IDs informados.
        Retorna dict: c100_id -> {campos...}
        """
        if not c100_ids:
            return {}

        resultados: Dict[int, Dict[str, Any]] = {}
        base = text(
            """
            SELECT
                c100.id     AS c100_id,
                c100.dt_doc AS dt_doc,
                c100.ind_emit AS ind_emit,
                c100.chv_nfe AS chv_nfe,
                c100.vl_frt AS vl_frt,
                c100.vl_seg AS vl_seg,
                c100.vl_out_da AS vl_out_da
            FROM registro_c100 c100
            WHERE c100.id IN :ids
            """
        ).bindparams(bindparam("ids", expanding=True))

        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size_in):
            rows = self.session.execute(base, {"ids": chunk}).mappings().all()
            for r in rows:
                resultados[r["c100_id"]] = dict(r)

        return resultados

    # =========================
    # 3) Produtos (0200)
    # =========================
    def produtos(self, cod_items: Sequence[str]) -> Dict[str, Dict[str, Any]]:
        """
        Busca dados do 0200 apenas para os códigos informados.
        Retorna dict: cod_item -> {cod_ncm, cod_cest}
        ATENÇÃO: se seu schema usa 'cest' ao invés de 'cod_cest', ajuste a query.
        """
        if not cod_items:
            return {}

        resultados: Dict[str, Dict[str, Any]] = {}
        base = text(
            """
            SELECT
                c0200.cod_item AS cod_item,
                c0200.cod_ncm  AS cod_ncm,
                c0200.cest     AS cod_cest
            FROM registro_0200 c0200
            WHERE c0200.empresa_id = :empresa_id
            AND c0200.cod_item IN :cods
            """
        ).bindparams(bindparam("cods", expanding=True))

        for chunk in self.chunks(list(set(filter(None, cod_items))), self.chunk_size_in):
            rows = self.session.execute(base, {"empresa_id": self.empresa_id, "cods": chunk}).mappings().all()
            for r in rows:
                resultados[r["cod_item"]] = dict(r)

        return resultados

    # =========================
    # 4) Soma por nota (para rateio)
    # =========================
    def calculo(self, c100_ids: Sequence[int]) -> Dict[int, float]:
        """
        Busca soma de vl_item por c100_id. Retorna: c100_id -> soma_itens
        """
        if not c100_ids:
            return {}

        resultado: Dict[int, float] = {}
        base = text(
            """
            SELECT c170.c100_id AS c100_id, SUM(c170.vl_item) AS soma_itens
            FROM registro_c170 c170
            WHERE c170.c100_id IN :ids
            GROUP BY c170.c100_id
            """
        ).bindparams(bindparam("ids", expanding=True))

        for chunk in self.chunks(list(set(c100_ids)), self.chunk_size_in):
            rows = self.session.execute(base, {"ids": chunk}).mappings().all()
            for r in rows:
                resultado[r["c100_id"]] = float(r["soma_itens"] or 0.0)

        return resultado

    # =========================
    # 5) Orquestração final
    # =========================
    def gerar(self) -> List[Any]:
        """
        Monta as linhas PNM chamando o builder, com dados já enriquecidos:
        - Item (C170)
        - Cabeçalho (C100)
        - Produto (0200)
        - Rateios (frete/seguro/outras) proporcionais ao vl_item/soma_itens
        """
        itens = self.itens()
        if not itens:
            return []

        c100_ids = [r["c100_id"] for r in itens if r.get("c100_id") is not None]
        cod_items = [r["cod_item"] for r in itens if r.get("cod_item")]

        cabecalhos = self.cabecalhos(c100_ids)
        produtos = self.produtos(cod_items)
        somas = self.calculo(c100_ids)

        linhas: List[Any] = []

        for it in itens:
            c100_id = it["c100_id"]
            head = cabecalhos.get(c100_id, {})
            prod = produtos.get(it.get("cod_item"), {})

            soma_itens = float(somas.get(c100_id, 0.0) or 0.0)
            vl_item = float(it.get("vl_item") or 0.0)

            proporcao = (vl_item / soma_itens) if soma_itens > 0 else 0.0
            vl_frt = float(head.get("vl_frt") or 0.0)
            vl_seg = float(head.get("vl_seg") or 0.0)
            vl_outras = float(head.get("vl_out_da") or 0.0)

            # Rateios arredondados a 2 casas (ajuste se o Fortes exigir outro padrão)
            frete_rateado = round(vl_frt * proporcao, 2)
            seguro_rateado = round(vl_seg * proporcao, 2)
            outras_desp_rateado = round(vl_outras * proporcao, 2)

            # Row enriquecida que o builderPNM vai consumir (e gerar string ou dict/df)
            row = {
                # --- C170 (item)
                **it,
                # --- C100 (cabeçalho)
                "dt_doc": head.get("dt_doc"),
                "ind_emit": head.get("ind_emit"),
                "chv_nfe": head.get("chv_nfe"),
                "vl_frt_cab": vl_frt,
                "vl_seg_cab": vl_seg,
                "vl_out_da_cab": vl_outras,
                # --- 0200 (produto)
                "cod_ncm": prod.get("cod_ncm"),
                # se sua coluna for 'cest' no DB, troque no SELECT do _fetch_produtos
                "cod_cest": prod.get("cod_cest"),
                # --- Rateios
                "frete_rateado": frete_rateado,
                "seguro_rateado": seguro_rateado,
                "outras_desp_rateado": outras_desp_rateado,
                # --- Auxiliares para o builder
                "soma_itens_nota": soma_itens,
                "proporcao_item_nota": proporcao,
            }

            linha = builderPNM(row)  # pode retornar string "PNM|...|" ou dict com 83 campos
            linhas.append(linha)

        return linhas
