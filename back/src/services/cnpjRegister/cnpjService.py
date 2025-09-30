import asyncio
from ...utils.cnpj import buscarInformacoesApi

class CnpjService:
    @staticmethod
    def consultarCnpj(cnpj: str) -> dict | None:
        try:
            resultado = asyncio.run(buscarInformacoesApi(cnpj))

            if not resultado:
                return None

            razao_social, _, uf, simples, _ = resultado

            return {
                "razao_social": razao_social,
                "cnpj": cnpj,
                "uf": uf,
                "simples": simples,
            }
        except Exception as e:
            print(f"[ERRO] Falha ao consultar CNPJ: {e}")
            return None