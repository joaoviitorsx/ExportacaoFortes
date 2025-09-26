from typing import Dict, Any
from src.utils.fsFormat import formatarValor, formatarData, tipoOperacao, modeloDoc, situacaoDoc

def builderNFM(dados: Dict[str, Any]) -> str:
    campos = [''] * 79

    campos[0] = "NFM"                                            # 1 - Tipo
    campos[1] = str(dados.get("num_doc", ''))                    # 2 - Código do Documento
    campos[2] = tipoOperacao(dados.get("ind_oper"))        # 3 - Tipo de Operação
    campos[3] = modeloDoc(dados.get("cod_mod"))            # 4 - Modelo do Documento
    campos[4] = "NF"                                             # 5 - Espécie do Documento
    campos[5] = str(dados.get("cod_part", ''))                   # 6 - Participante
    campos[6] = str(dados.get("ser", ''))                        # 7 - Série
    campos[8] = str(dados.get("num_doc", ''))                    # 9 - Número do Documento
    
    campos[10] = formatarData(dados.get("dt_doc"))               # 11 - Data de Emissão
    campos[11] = formatarData(dados.get("dt_e_s"))               # 12 - Data de Entrada/Saída
    
    campos[19] = situacaoDoc(dados.get("cod_sit"))          # 20 - Situação do Documento
    campos[20] = formatarValor(dados.get("vl_doc"))              # 21 - Valor Total do Documento
    campos[22] = formatarValor(dados.get("vl_desc"))             # 23 - Valor do Desconto
    campos[23] = formatarValor(dados.get("vl_merc"))             # 24 - Valor das Mercadorias
    campos[25] = formatarValor(dados.get("vl_frt"))              # 26 - Valor do Frete
    campos[26] = formatarValor(dados.get("vl_seg"))              # 27 - Valor do Seguro
    campos[27] = formatarValor(dados.get("vl_out_da"))           # 28 - Outras Despesas
    
    campos[28] = formatarValor(dados.get("vl_bc_icms"))          # 29 - Base de Cálculo do ICMS
    campos[29] = formatarValor(dados.get("vl_icms"))             # 30 - Valor do ICMS
    campos[30] = formatarValor(dados.get("vl_bc_icms_st"))       # 31 - Base de Cálculo do ICMS ST
    campos[31] = formatarValor(dados.get("vl_icms_st"))          # 32 - Valor do ICMS ST
    campos[32] = formatarValor(dados.get("vl_ipi"))              # 33 - Valor do IPI
    campos[33] = formatarValor(dados.get("vl_pis"))              # 34 - Valor do PIS
    campos[34] = formatarValor(dados.get("vl_cofins"))           # 35 - Valor da COFINS

    campos[44] = str(dados.get("chv_nfe", ''))                   # 45 - Chave Eletrônica
    # campo[45] é Informações Complementares (deixado em branco)
    
    campos[61] = str(dados.get("ind_frt", ''))                   # 62 - Tipo de Frete

    return "|".join(campos)