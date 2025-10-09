from datetime import datetime
from typing import Dict, Any
from ....utils.fsFormat import formatarData

def builderCAB(empresa: Dict[str, Any], registro_0000: Dict[str, Any]) -> str:
    tipo_registro = "CAB"
    versao_leiaute = "172"
    software = "AssertivusContabil"[:62]
    data_geracao = datetime.now().strftime("%Y%m%d")
    nome_empresa = str(empresa.get("razao_social", ''))[:15]
    data_inicial = formatarData(registro_0000.get("dt_ini")) 
    data_final = formatarData(registro_0000.get("dt_fin"))
    periodo_formatado = str(registro_0000.get('periodo', '')).replace('/', '')
    descricao = f"ENTRADAS {nome_empresa} {periodo_formatado}"[:40] 
    #aliquotas_especificas_flag = empresa.get("aliq_espec", False)
    flag_aliq_especificas = "S"

    linha_cab = "|".join([
        tipo_registro,
        versao_leiaute,
        software,
        data_geracao,
        nome_empresa,
        data_inicial,
        data_final,
        descricao,
        flag_aliq_especificas
    ])
    
    return linha_cab + "|"