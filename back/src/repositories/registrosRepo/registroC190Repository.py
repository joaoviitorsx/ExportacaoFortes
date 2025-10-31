from sqlalchemy import text
from ...utils.fsFormat import escapeString

class RegistroC190Repository:
    def __init__(self, session):
        self.session = session

    def salvamento(self, lote: list[dict]):
        if not lote:
            return

        try:
            dados_preparados = []
            
            for item in lote:
                dados_preparados.append({
                    'c100_id': item.get('c100_id'),
                    'doc_key': escapeString(item.get('doc_key', '')),
                    'empresa_id': item['empresa_id'],
                    'periodo': item['periodo'],
                    'reg': item.get('reg', 'C190'),
                    'cst_icms': item.get('cst_icms', ''),
                    'cfop': item.get('cfop', ''),
                    'aliq_icms': float(item.get('aliq_icms', 0)),
                    'vl_opr': float(item.get('vl_opr', 0)),
                    'vl_bc_icms': float(item.get('vl_bc_icms', 0)),
                    'vl_icms': float(item.get('vl_icms', 0)),
                    'vl_bc_icms_st': float(item.get('vl_bc_icms_st', 0)),
                    'vl_icms_st': float(item.get('vl_icms_st', 0)),
                    'vl_red_bc': float(item.get('vl_red_bc', 0)),
                    'vl_ipi': float(item.get('vl_ipi', 0)),
                    'cod_obs': item.get('cod_obs', ''),
                    'ativo': 1
                })

            query = text("""
                INSERT INTO registro_c190 (
                    c100_id, doc_key, empresa_id, periodo, reg, cst_icms, cfop,
                    aliq_icms, vl_opr, vl_bc_icms, vl_icms, vl_bc_icms_st,
                    vl_icms_st, vl_red_bc, vl_ipi, cod_obs, ativo
                )
                VALUES (
                    :c100_id, :doc_key, :empresa_id, :periodo, :reg, :cst_icms, :cfop,
                    :aliq_icms, :vl_opr, :vl_bc_icms, :vl_icms, :vl_bc_icms_st,
                    :vl_icms_st, :vl_red_bc, :vl_ipi, :cod_obs, :ativo
                )
            """)

            resultado = self.session.execute(query, dados_preparados)
            print(f"[DEBUG C190] {resultado.rowcount} registros inseridos")

        except Exception as e:
            print(f"[ERRO C190Repository.salvamento] {e}")
            import traceback
            traceback.print_exc()
            raise