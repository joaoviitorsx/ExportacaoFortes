import pandas as pd
from .....src.utils.sanitizacao import sanitizarCampo
from .....src.services.etl.validadorService import ValidadorService

class Registro0200Service:
    def __init__(self, session, empresa_id):
        self.session = session
        self.empresa_id = empresa_id
        self.lote = []
        self.periodo = None
        self.tabela = "registro_0200"
        self.nome = "0200"
        self.cod_item_atual = None

    def set_context(self, periodo, filial):
        self.periodo = periodo
        self.filial = filial

    def processar(self, partes: list[str]):
        if not self.periodo:
            raise ValueError("Contexto do período não definido para registro 0200.")

        partes = (partes + [None] * 13)[:13]

        cod_item = partes[1]

        dados = {
            "reg": partes[0],
            "cod_item": sanitizarCampo("cod_item", cod_item),
            "descr_item": sanitizarCampo("descr_item", partes[2]),
            "cod_barra": partes[3],
            "cod_ant_item": partes[4],
            "unid_inv": sanitizarCampo("unid_inv", partes[5]),
            "tipo_item": partes[6],
            "cod_ncm": partes[7],
            "ex_ipi": partes[8],
            "cod_gen": partes[9],
            "cod_list": partes[10],
            "aliq_icms": sanitizarCampo("aliq_icms", partes[11]) if partes[11] not in (None, '', ' ') else 0.00,
            "cest": partes[12],
            "periodo": self.periodo,
            "empresa_id": self.empresa_id,
            "ativo": True
        }
        tipo_item = str(dados.get("tipo_item") or "").zfill(2)
        cod_list = str(dados.get("cod_list") or "").strip()
        if not dados.get("cod_ncm") and tipo_item not in ("09", "99") and not cod_list:
            print(f"[WARN 0200] cod_ncm vazio: cod_item={dados.get('cod_item')} tipo_item={tipo_item} cod_list={cod_list}")
        ok, erros = ValidadorService.validarRegistro0200(dados)
        if ok:
            self.cod_item_atual = dados["cod_item"]
            self.lote.append(dados)
        else:
            print(f"[WARN 0200] Registro ignorado: cod_item={dados.get('cod_item')} erros={erros}")
            return

    def toDataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.lote)
