import aiohttp
import asyncio
import ssl
import sys
import os

from ..utils.cache import cache
from ..utils.validadores import removedorCaracteres

CNAES_VALIDOS = {
    '4623108', '4623199', '4632001', '4637107', '4639701', '4639702',
    '4646002', '4647801', '4649408', '4635499', '4637102', '4637199',
    '4644301', '4632003', '4691500', '4693100', '3240099', '4649499',
    '8020000', '4711301', '4711302', '4712100', '4721103', '4721104',
    '4729699', '4761003', '4789005', '4771701', '4771702', '4771703',
    '4772500', '4763601'
}

@cache()
async def buscarInformacoes(cnpj: str, tentativas: int = 5) -> tuple[str, str, str, bool, bool] | tuple[None, None, None, None, None]:

    cnpj = removedorCaracteres(cnpj.strip())
    if len(cnpj) != 14:
        raise ValueError("CNPJ inválido: deve conter 14 dígitos")

    url = f"https://minhareceita.org/{cnpj}"
    timeout = aiohttp.ClientTimeout(total=30)

    connector = aiohttp.TCPConnector(
        ssl=False,
        ttl_dns_cache=300
    )

    for tentativa in range(1, tentativas + 1):
        try:
            async with aiohttp.ClientSession(
                timeout=timeout,
                connector=connector
            ) as session:

                async with session.get(url) as response:
                    if response.status != 200:
                        print(
                            f"[API Error] Status {response.status} "
                            f"(tentativa {tentativa}/{tentativas})"
                        )
                        continue

                    dados = await response.json()

                    razao_social = dados.get("razao_social", "").strip()
                    cnae_codigo = str(dados.get("cnae_fiscal", "")).strip()
                    uf = dados.get("uf", "").strip().upper()
                    simples = bool(dados.get("opcao_pelo_simples", False))

                    if not all([razao_social, cnae_codigo, uf]):
                        raise ValueError("Dados incompletos retornados da API")

                    decreto = (uf == "CE" and cnae_codigo in CNAES_VALIDOS)

                    return (
                        razao_social,
                        cnae_codigo,
                        uf,
                        simples,
                        decreto
                    )

        except asyncio.TimeoutError:
            print(
                f"[Timeout] API demorou a responder "
                f"(tentativa {tentativa}/{tentativas})"
            )

        except aiohttp.ClientError as e:
            print(
                f"[HTTP Error] {e} "
                f"(tentativa {tentativa}/{tentativas})"
            )

        except Exception as e:
            print(
                f"[Erro Geral] {e} "
                f"(tentativa {tentativa}/{tentativas})"
            )

        await asyncio.sleep(1)

    return None, None, None, None, None

async def buscarInformacoesApi(cnpj: str) -> tuple | None:
    try:
        return await buscarInformacoes(cnpj)
    except Exception as e:
        print(f"[Erro] Falha ao consultar CNPJ {cnpj}: {e}")
        return None

async def processarCnpjs(lista_cnpjs: list[str]) -> dict[str, tuple]:
    tarefas = [buscarInformacoes(cnpj) for cnpj in lista_cnpjs]
    resultados = await asyncio.gather(*tarefas, return_exceptions=False)
    return dict(zip(lista_cnpjs, resultados))
