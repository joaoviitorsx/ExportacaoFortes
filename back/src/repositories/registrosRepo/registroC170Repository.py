from sqlalchemy import text
from ...utils.fsFormat import escapeString

class RegistroC170Repository:
    def __init__(self, session):
        self.session = session

    def salvamento(self, lote: list[dict]):
        """Salva lote de registros C170"""
        if not lote:
            return

        try:
            # Construir query de inserção em lote
            valores = []
            for item in lote:
                # *** CORREÇÃO: Garantir que todos os valores numéricos sejam float ***
                valores.append(f"""(
                    {item.get('c100_id')},
                    '{escapeString(item.get('doc_key', ''))}',
                    {item['empresa_id']},
                    '{item['periodo']}',
                    '{item.get('reg', 'C170')}',
                    '{item.get('num_item', '')}',
                    '{escapeString(item.get('cod_item', ''))}',
                    '{escapeString(item.get('descr_compl', ''))}',
                    {float(item.get('qtd', 0))},
                    '{item.get('unid', '')}',
                    {float(item.get('vl_item', 0))},
                    {float(item.get('vl_desc', 0))},
                    '{item.get('ind_mov', '')}',
                    '{item.get('cst_icms', '')}',
                    '{item.get('cfop', '')}',
                    '{item.get('cod_nat', '')}',
                    {float(item.get('vl_bc_icms', 0))},
                    {float(item.get('aliq_icms', 0))},
                    {float(item.get('vl_icms', 0))},
                    {float(item.get('vl_bc_icms_st', 0))},
                    {float(item.get('aliq_st', 0))},
                    {float(item.get('vl_icms_st', 0))},
                    '{item.get('ind_apur', '')}',
                    '{item.get('cst_ipi', '')}',
                    '{item.get('cod_enq', '')}',
                    {float(item.get('vl_bc_ipi', 0))},
                    {float(item.get('aliq_ipi', 0))},
                    {float(item.get('vl_ipi', 0))},
                    '{item.get('cst_pis', '')}',
                    {float(item.get('vl_bc_pis', 0))},
                    {float(item.get('aliq_pis', 0))},
                    {float(item.get('quant_bc_pis', 0))},
                    {float(item.get('aliq_pis_reais', 0))},
                    {float(item.get('vl_pis', 0))},
                    '{item.get('cst_cofins', '')}',
                    {float(item.get('vl_bc_cofins', 0))},
                    {float(item.get('aliq_cofins', 0))},
                    {float(item.get('quant_bc_cofins', 0))},
                    {float(item.get('aliq_cofins_reais', 0))},
                    {float(item.get('vl_cofins', 0))},
                    '{item.get('cod_cta', '')}',
                    {float(item.get('vl_abat_nt', 0))},
                    '{item.get('filial', '')}',
                    {1 if item.get('ativo', True) else 0}
                )""")

            query = f"""
                INSERT INTO registro_c170 (
                    c100_id, doc_key, empresa_id, periodo, reg, num_item, cod_item, descr_compl,
                    qtd, unid, vl_item, vl_desc, ind_mov, cst_icms, cfop, cod_nat,
                    vl_bc_icms, aliq_icms, vl_icms, vl_bc_icms_st, aliq_st, vl_icms_st,
                    ind_apur, cst_ipi, cod_enq, vl_bc_ipi, aliq_ipi, vl_ipi,
                    cst_pis, vl_bc_pis, aliq_pis, quant_bc_pis, aliq_pis_reais, vl_pis,
                    cst_cofins, vl_bc_cofins, aliq_cofins, quant_bc_cofins, aliq_cofins_reais,
                    vl_cofins, cod_cta, vl_abat_nt, filial, ativo
                )
                VALUES {', '.join(valores)}
            """

            self.session.execute(text(query))

        except Exception as e:
            print(f"[ERRO C170Repository.salvamento] {e}")
            import traceback
            traceback.print_exc()
            raise
