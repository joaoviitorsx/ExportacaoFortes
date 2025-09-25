from datetime import datetime

def builderCAB(empresa, registro_0000):
    tipo_registro = "CAB"
    versao_leiaute = "189"
    software = "RSFiscal"
    data_geracao = datetime.now().strftime("%Y%m%d")
    nome_empresa = empresa["razao_social"]
    data_inicial = str(registro_0000["dt_ini"]).replace("-", "") if registro_0000.get("dt_ini") else ""
    data_final = str(registro_0000["dt_fin"]).replace("-", "") if registro_0000.get("dt_fin") else ""
    descricao = f"ENTRADAS {empresa['razao_social']} {registro_0000.get('periodo', '').replace('/', '')}"
    optante_simples = "S" if empresa.get("simples") else "N"

    return f"{tipo_registro}|{versao_leiaute}|{software}|{data_geracao}|{nome_empresa}|{data_inicial}|{data_final}|{descricao}|{optante_simples}"