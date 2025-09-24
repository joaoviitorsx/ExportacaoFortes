import pandas as pd
from sqlalchemy import text

class RegistroC100Repository:
    def __init__(self, session):
        self.session = session

    def salvamento(self, registros: list[dict]):
        if not registros:
            return

        df = pd.DataFrame(registros)

        colunas = [
            "empresa_id", "periodo", "reg", "ind_oper", "ind_emit", "cod_part", "cod_mod",
            "cod_sit", "ser", "num_doc", "chv_nfe", "dt_doc", "dt_e_s", "vl_doc", "ind_pgto",
            "vl_desc", "vl_abat_nt", "vl_merc", "ind_frt", "vl_frt", "vl_seg", "vl_out_da",
            "vl_bc_icms", "vl_icms", "vl_bc_icms_st", "vl_icms_st", "vl_ipi", "vl_pis",
            "vl_cofins", "vl_pis_st", "vl_cofins_st", "filial", "ativo"
        ]
        df = df.reindex(columns=colunas)

        try:
            df.to_sql(
                "registro_c100",
                self.session.bind,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=5000
            )
        except Exception as e:
            self.session.rollback()
            print(f"[ERRO] Falha ao salvar registros C100: {e}")
            raise

    def buscarIDS(self, periodo: str, empresa_id: int):
        query = text("""
            SELECT id, num_doc, ind_oper, cod_part, chv_nfe
            FROM registro_c100
            WHERE periodo = :periodo 
            AND empresa_id = :empresa_id 
            AND ativo = 1
        """)
        result = self.session.execute(query, {
            "periodo": periodo,
            "empresa_id": empresa_id
        })
        return [dict(row._mapping) for row in result]


