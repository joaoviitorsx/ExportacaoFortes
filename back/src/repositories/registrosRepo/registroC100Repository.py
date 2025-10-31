from sqlalchemy import text
from ...utils.fsFormat import floatC100, escapeString


class RegistroC100Repository:
    def __init__(self, session):
        self.session = session

    def salvamento(self, lote: list[dict]):
        if not lote:
            return

        try:
            dados_preparados = []
            for item in lote:
                dados_preparados.append({
                    'empresa_id': item['empresa_id'],
                    'periodo': item['periodo'],
                    'reg': item.get('reg', 'C100'),
                    'ind_oper': item.get('ind_oper', ''),
                    'ind_emit': item.get('ind_emit', ''),
                    'cod_part': escapeString(item.get('cod_part', ''))[:60],
                    'cod_mod': item.get('cod_mod', ''),
                    'cod_sit': item.get('cod_sit', ''),
                    'ser': item.get('ser', ''),
                    'num_doc': item.get('num_doc', ''),
                    'chv_nfe': escapeString(item.get('chv_nfe', ''))[:44],
                    'doc_key': escapeString(item.get('doc_key', ''))[:255],
                    'dt_doc': item.get('dt_doc'),
                    'dt_e_s': item.get('dt_e_s'),
                    'vl_doc': floatC100(item.get('vl_doc', 0)),
                    'ind_pgto': item.get('ind_pgto', ''),
                    'vl_desc': floatC100(item.get('vl_desc', 0)),
                    'vl_abat_nt': floatC100(item.get('vl_abat_nt', 0)),
                    'vl_merc': floatC100(item.get('vl_merc', 0)),
                    'ind_frt': item.get('ind_frt', ''),
                    'vl_frt': floatC100(item.get('vl_frt', 0)),
                    'vl_seg': floatC100(item.get('vl_seg', 0)),
                    'vl_out_da': floatC100(item.get('vl_out_da', 0)),
                    'vl_bc_icms': floatC100(item.get('vl_bc_icms', 0)),
                    'vl_icms': floatC100(item.get('vl_icms', 0)),
                    'vl_bc_icms_st': floatC100(item.get('vl_bc_icms_st', 0)),
                    'vl_icms_st': floatC100(item.get('vl_icms_st', 0)),
                    'vl_ipi': floatC100(item.get('vl_ipi', 0)),
                    'vl_pis': floatC100(item.get('vl_pis', 0)),
                    'vl_cofins': floatC100(item.get('vl_cofins', 0)),
                    'vl_pis_st': floatC100(item.get('vl_pis_st', 0)),
                    'vl_cofins_st': floatC100(item.get('vl_cofins_st', 0)),
                    'filial': item.get('filial', ''),
                    'ativo': 1
                })

            query_insert = text("""
                INSERT INTO registro_c100 (
                    empresa_id, periodo, reg, ind_oper, ind_emit, cod_part, cod_mod, cod_sit,
                    ser, num_doc, chv_nfe, doc_key, dt_doc, dt_e_s, vl_doc, ind_pgto, vl_desc,
                    vl_abat_nt, vl_merc, ind_frt, vl_frt, vl_seg, vl_out_da, vl_bc_icms,
                    vl_icms, vl_bc_icms_st, vl_icms_st, vl_ipi, vl_pis, vl_cofins,
                    vl_pis_st, vl_cofins_st, filial, ativo
                )
                VALUES (
                    :empresa_id, :periodo, :reg, :ind_oper, :ind_emit, :cod_part, :cod_mod, :cod_sit,
                    :ser, :num_doc, :chv_nfe, :doc_key, :dt_doc, :dt_e_s, :vl_doc, :ind_pgto, :vl_desc,
                    :vl_abat_nt, :vl_merc, :ind_frt, :vl_frt, :vl_seg, :vl_out_da, :vl_bc_icms,
                    :vl_icms, :vl_bc_icms_st, :vl_icms_st, :vl_ipi, :vl_pis, :vl_cofins,
                    :vl_pis_st, :vl_cofins_st, :filial, :ativo
                )
            """)

            self.session.execute(query_insert, dados_preparados)
            self.session.commit()
            print(f"[DEBUG C100] {len(dados_preparados)} registros inseridos")

        except Exception as e:
            self.session.rollback()
            raise RuntimeError(f"Erro ao salvar registros C100: {e}")

    def buscarIDS(self, periodo: str, empresa_id: int) -> list[dict]:
        try:
            query = text("""
                SELECT id, doc_key
                FROM registro_c100
                WHERE empresa_id = :empresa_id AND periodo = :periodo
            """)
            result = self.session.execute(query, {"empresa_id": empresa_id, "periodo": periodo})
            return [{"id": row[0], "doc_key": row[1]} for row in result]
        except Exception:
            return []
