from sqlalchemy import text
from ...utils.fsFormat import escapeString

class RegistroC170Repository:
    def __init__(self, session):
        self.session = session

    def salvamento(self, lote: list[dict]):
        if not lote:
            return

        try:
            dados_preparados = []
            
            for item in lote:
                cod_item = item.get('cod_item', '')
                cod_item = cod_item.lstrip('0') if cod_item else ''
                
                dados_preparados.append({
                    'c100_id': item.get('c100_id'),
                    'doc_key': escapeString(item.get('doc_key', '')),
                    'empresa_id': item['empresa_id'],
                    'periodo': item['periodo'],
                    'reg': item.get('reg', 'C170'),
                    'num_item': item.get('num_item', ''),
                    'cod_item': escapeString(cod_item),
                    'descr_compl': escapeString(item.get('descr_compl', '')),
                    'qtd': float(item.get('qtd', 0)),
                    'unid': item.get('unid', ''),
                    'vl_item': float(item.get('vl_item', 0)),
                    'vl_desc': float(item.get('vl_desc', 0)),
                    'ind_mov': item.get('ind_mov', ''),
                    'cst_icms': item.get('cst_icms', ''),
                    'cfop': item.get('cfop', ''),
                    'cod_nat': item.get('cod_nat', ''),
                    'vl_bc_icms': float(item.get('vl_bc_icms', 0)),
                    'aliq_icms': float(item.get('aliq_icms', 0)),
                    'vl_icms': float(item.get('vl_icms', 0)),
                    'vl_bc_icms_st': float(item.get('vl_bc_icms_st', 0)),
                    'aliq_st': float(item.get('aliq_st', 0)),
                    'vl_icms_st': float(item.get('vl_icms_st', 0)),
                    'ind_apur': item.get('ind_apur', ''),
                    'cst_ipi': item.get('cst_ipi', ''),
                    'cod_enq': item.get('cod_enq', ''),
                    'vl_bc_ipi': float(item.get('vl_bc_ipi', 0)),
                    'aliq_ipi': float(item.get('aliq_ipi', 0)),
                    'vl_ipi': float(item.get('vl_ipi', 0)),
                    'cst_pis': item.get('cst_pis', ''),
                    'vl_bc_pis': float(item.get('vl_bc_pis', 0)),
                    'aliq_pis': float(item.get('aliq_pis', 0)),
                    'quant_bc_pis': float(item.get('quant_bc_pis', 0)),
                    'aliq_pis_reais': float(item.get('aliq_pis_reais', 0)),
                    'vl_pis': float(item.get('vl_pis', 0)),
                    'cst_cofins': item.get('cst_cofins', ''),
                    'vl_bc_cofins': float(item.get('vl_bc_cofins', 0)),
                    'aliq_cofins': float(item.get('aliq_cofins', 0)),
                    'quant_bc_cofins': float(item.get('quant_bc_cofins', 0)),
                    'aliq_cofins_reais': float(item.get('aliq_cofins_reais', 0)),
                    'vl_cofins': float(item.get('vl_cofins', 0)),
                    'cod_cta': item.get('cod_cta', ''),
                    'vl_abat_nt': float(item.get('vl_abat_nt', 0)),
                    'filial': item.get('filial', ''),
                    'ativo': 1
                })

            query = text("""
                INSERT INTO registro_c170 (
                    c100_id, doc_key, empresa_id, periodo, reg, num_item, cod_item, descr_compl,
                    qtd, unid, vl_item, vl_desc, ind_mov, cst_icms, cfop, cod_nat,
                    vl_bc_icms, aliq_icms, vl_icms, vl_bc_icms_st, aliq_st, vl_icms_st,
                    ind_apur, cst_ipi, cod_enq, vl_bc_ipi, aliq_ipi, vl_ipi,
                    cst_pis, vl_bc_pis, aliq_pis, quant_bc_pis, aliq_pis_reais, vl_pis,
                    cst_cofins, vl_bc_cofins, aliq_cofins, quant_bc_cofins, aliq_cofins_reais,
                    vl_cofins, cod_cta, vl_abat_nt, filial, ativo
                )
                VALUES (
                    :c100_id, :doc_key, :empresa_id, :periodo, :reg, :num_item, :cod_item, :descr_compl,
                    :qtd, :unid, :vl_item, :vl_desc, :ind_mov, :cst_icms, :cfop, :cod_nat,
                    :vl_bc_icms, :aliq_icms, :vl_icms, :vl_bc_icms_st, :aliq_st, :vl_icms_st,
                    :ind_apur, :cst_ipi, :cod_enq, :vl_bc_ipi, :aliq_ipi, :vl_ipi,
                    :cst_pis, :vl_bc_pis, :aliq_pis, :quant_bc_pis, :aliq_pis_reais, :vl_pis,
                    :cst_cofins, :vl_bc_cofins, :aliq_cofins, :quant_bc_cofins, :aliq_cofins_reais,
                    :vl_cofins, :cod_cta, :vl_abat_nt, :filial, :ativo
                )
            """)

            resultado = self.session.execute(query, dados_preparados)
            print(f"[DEBUG C170] {resultado.rowcount} registros inseridos")

        except Exception as e:
            print(f"[ERRO C170Repository.salvamento] {e}")
            import traceback
            traceback.print_exc()
            raise