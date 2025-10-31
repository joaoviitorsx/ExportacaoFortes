from sqlalchemy import text
from ...utils.fsFormat import floatC100, escapeString

class RegistroC100Repository:
    def __init__(self, session):
        self.session = session

    def salvamento(self, lote: list[dict]):
        if not lote:
            return

        try:
            valores = []
            itens_problematicos = []
            
            for idx, item in enumerate(lote):
                try:
                    vl_doc = floatC100(item.get('vl_doc', 0))
                    vl_desc = floatC100(item.get('vl_desc', 0))
                    vl_abat_nt = floatC100(item.get('vl_abat_nt', 0))
                    vl_merc = floatC100(item.get('vl_merc', 0))
                    vl_frt = floatC100(item.get('vl_frt', 0))
                    vl_seg = floatC100(item.get('vl_seg', 0))
                    vl_out_da = floatC100(item.get('vl_out_da', 0))
                    vl_bc_icms = floatC100(item.get('vl_bc_icms', 0))
                    vl_icms = floatC100(item.get('vl_icms', 0))
                    vl_bc_icms_st = floatC100(item.get('vl_bc_icms_st', 0))
                    vl_icms_st = floatC100(item.get('vl_icms_st', 0))
                    vl_ipi = floatC100(item.get('vl_ipi', 0))
                    vl_pis = floatC100(item.get('vl_pis', 0))
                    vl_cofins = floatC100(item.get('vl_cofins', 0))
                    vl_pis_st = floatC100(item.get('vl_pis_st', 0))
                    vl_cofins_st = floatC100(item.get('vl_cofins_st', 0))
                    
                    # Validar strings
                    cod_part = escapeString(item.get('cod_part', ''))
                    chv_nfe = escapeString(item.get('chv_nfe', ''))
                    doc_key = escapeString(item.get('doc_key', ''))
                    
                    # Validar tamanhos
                    if len(cod_part) > 60:
                        cod_part = cod_part[:60]
                    
                    if len(chv_nfe) > 44:
                        chv_nfe = chv_nfe[:44]
                    
                    if len(doc_key) > 255:
                        doc_key = doc_key[:255]
                    
                    valores.append(f"""(
                        {item['empresa_id']},
                        '{item['periodo']}',
                        '{item.get('reg', 'C100')}',
                        '{item.get('ind_oper', '')}',
                        '{item.get('ind_emit', '')}',
                        '{cod_part}',
                        '{item.get('cod_mod', '')}',
                        '{item.get('cod_sit', '')}',
                        '{item.get('ser', '')}',
                        '{item.get('num_doc', '')}',
                        '{chv_nfe}',
                        '{doc_key}',
                        {f"'{item.get('dt_doc')}'" if item.get('dt_doc') else 'NULL'},
                        {f"'{item.get('dt_e_s')}'" if item.get('dt_e_s') else 'NULL'},
                        {vl_doc},
                        '{item.get('ind_pgto', '')}',
                        {vl_desc},
                        {vl_abat_nt},
                        {vl_merc},
                        '{item.get('ind_frt', '')}',
                        {vl_frt},
                        {vl_seg},
                        {vl_out_da},
                        {vl_bc_icms},
                        {vl_icms},
                        {vl_bc_icms_st},
                        {vl_icms_st},
                        {vl_ipi},
                        {vl_pis},
                        {vl_cofins},
                        {vl_pis_st},
                        {vl_cofins_st},
                        '{item.get('filial', '')}',
                        {1 if item.get('ativo', True) else 0}
                    )""")
                    
                except Exception as e:
                    erro_msg = f"Item #{idx}: {e}"
                    itens_problematicos.append({
                        'idx': idx,
                        'num_doc': item.get('num_doc'),
                        'chv_nfe': item.get('chv_nfe', '')[:50],
                        'erro': str(e)
                    })
                    print(f"[ERRO] {erro_msg}")
                    continue

            if not valores:
                print(f"[AVISO] Nenhum registro válido para inserir")
                if itens_problematicos:
                    print(f"[ERRO] {len(itens_problematicos)} itens problemáticos:")
                    for item_prob in itens_problematicos[:5]:
                        print(f"   - Item #{item_prob['idx']}: {item_prob['erro']}")
                return

            # *** INSERÇÃO COM INSERT IGNORE PARA EVITAR DUPLICATAS ***
            tamanho_lote = 100
            total_inseridos = 0
            total_duplicados = 0
            
            for i in range(0, len(valores), tamanho_lote):
                lote_atual = valores[i:i + tamanho_lote]
                
                # *** USANDO INSERT IGNORE PARA IGNORAR DUPLICATAS ***
                query = f"""
                    INSERT IGNORE INTO registro_c100 (
                        empresa_id, periodo, reg, ind_oper, ind_emit, cod_part, cod_mod, cod_sit,
                        ser, num_doc, chv_nfe, doc_key, dt_doc, dt_e_s, vl_doc, ind_pgto, vl_desc,
                        vl_abat_nt, vl_merc, ind_frt, vl_frt, vl_seg, vl_out_da, vl_bc_icms,
                        vl_icms, vl_bc_icms_st, vl_icms_st, vl_ipi, vl_pis, vl_cofins,
                        vl_pis_st, vl_cofins_st, filial, ativo
                    )
                    VALUES {', '.join(lote_atual)}
                """
                
                try:
                    resultado = self.session.execute(text(query))
                    inseridos_neste_lote = resultado.rowcount
                    duplicados_neste_lote = len(lote_atual) - inseridos_neste_lote
                    
                    total_inseridos += inseridos_neste_lote
                    total_duplicados += duplicados_neste_lote
                    
                    print(f"[DEBUG] Lote {i//tamanho_lote + 1}: {inseridos_neste_lote} inseridos, {duplicados_neste_lote} duplicados")
                    
                except Exception as e_lote:
                    print(f"[ERRO] Falha no lote {i//tamanho_lote + 1}: {e_lote}")
                    
                    # Salvar lote problemático
                    with open(f'erro_c100_lote_{i//tamanho_lote + 1}.sql', 'w', encoding='utf-8') as f:
                        f.write(query)
                    print(f"[DEBUG] Query problemática salva em erro_c100_lote_{i//tamanho_lote + 1}.sql")
                    raise

            print(f"[DEBUG] Total: {total_inseridos} inseridos, {total_duplicados} duplicados (ignorados)")

        except Exception as e:
            print(f"[ERRO C100Repository.salvamento] {e}")
            import traceback
            traceback.print_exc()
            raise

    def buscarIDS(self, periodo: str, empresa_id: int) -> list[dict]:
        """
        Busca IDs e doc_keys dos registros C100 do período.
        - Não filtra por ativo=TRUE porque os registros podem estar com ativo=FALSE após soft delete
        - Retorna lista de dicts com 'id' e 'doc_key'
        """
        try:
            query = text("""
                SELECT id, doc_key
                FROM registro_c100
                WHERE empresa_id = :empresa_id 
                  AND periodo = :periodo
            """)

            result = self.session.execute(
                query,
                {"empresa_id": empresa_id, "periodo": periodo}
            )

            # Converter resultado em lista de dicts
            rows = []
            for row in result:
                rows.append({
                    "id": row[0],
                    "doc_key": row[1]
                })

            print(f"[DEBUG buscarIDS] Encontrados {len(rows)} registros C100 (incluindo inativos)")
            if rows and len(rows) <= 3:
                for r in rows[:3]:
                    print(f"   ID={r['id']}, doc_key={r['doc_key'][:50]}...")

            return rows

        except Exception as e:
            print(f"[ERRO C100Repository.buscarIDS] {e}")
            import traceback
            traceback.print_exc()
            return []

    