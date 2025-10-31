from sqlalchemy import text
from ...utils.fsFormat import escapeString

class RegistroC190Repository:
    def __init__(self, session):
        self.session = session

    def salvamento(self, lote: list[dict]):
        if not lote:
            return

        try:
            # Construir query de inserção em lote
            valores = []
            for item in lote:
                valores.append(f"""(
                    {item.get('c100_id')},
                    '{escapeString(item.get('doc_key', ''))}',
                    {item['empresa_id']},
                    '{item['periodo']}',
                    '{item.get('reg', 'C190')}',
                    '{item.get('cst_icms', '')}',
                    '{item.get('cfop', '')}',
                    {float(item.get('aliq_icms', 0))},
                    {float(item.get('vl_opr', 0))},
                    {float(item.get('vl_bc_icms', 0))},
                    {float(item.get('vl_icms', 0))},
                    {float(item.get('vl_bc_icms_st', 0))},
                    {float(item.get('vl_icms_st', 0))},
                    {float(item.get('vl_red_bc', 0))},
                    {float(item.get('vl_ipi', 0))},
                    '{item.get('cod_obs', '')}',
                    {1 if item.get('ativo', True) else 0}
                )""")

            query = f"""
                INSERT INTO registro_c190 (
                    c100_id, doc_key, empresa_id, periodo, reg, cst_icms, cfop,
                    aliq_icms, vl_opr, vl_bc_icms, vl_icms, vl_bc_icms_st,
                    vl_icms_st, vl_red_bc, vl_ipi, cod_obs, ativo
                )
                VALUES {', '.join(valores)}
            """

            self.session.execute(text(query))

        except Exception as e:
            print(f"[ERRO C190Repository.salvamento] {e}")
            import traceback
            traceback.print_exc()
            raise