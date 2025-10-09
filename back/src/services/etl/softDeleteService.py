import re
from sqlalchemy import text

class SoftDeleteService:

    @staticmethod
    def softDelete(session, empresa_id: int, periodo: str):
        tabelas = ["registro_0000", "registro_0150", "registro_0200","registro_c100", "registro_c170", "registro_c190"]
            
        for tabela in tabelas:
            sql = text(f"""
                UPDATE {tabela}
                SET ativo = 0
                WHERE empresa_id = :empresa_id
                AND periodo = :periodo
                AND ativo = 1
            """)
            session.execute(sql, {"empresa_id": empresa_id, "periodo": periodo})

        session.commit()

    @staticmethod
    def extrairPeriodo(arquivos: list[str]) -> str:
        if not arquivos:
            raise ValueError("Lista de arquivos vazia.")

        periodosEncontrados = set()

        for caminho in arquivos:
            encodings = ["latin-1", "utf-8", "utf-16", "cp1252"]
            for enc in encodings:
                try:
                    with open(caminho, "r", encoding=enc, errors="ignore") as f:
                        primeiraLinha = f.readline().strip()
                        if primeiraLinha.startswith("|0000|"):
                            partes = primeiraLinha.split("|")
                            if len(partes) > 4:
                                data_ini = partes[4]

                                if re.match(r"\d{8}", data_ini):
                                    mes = data_ini[2:4]
                                    ano = data_ini[4:]
                                    periodo = f"{mes}/{ano}"
                                    periodosEncontrados.add(periodo)
                                    break
                except Exception:
                    continue

        if not periodosEncontrados:
            raise ValueError("Nenhum período válido foi encontrado nos arquivos SPED.")

        if len(periodosEncontrados) > 1:
            raise ValueError(f"Os arquivos contêm períodos diferentes: {periodosEncontrados}")

        return periodosEncontrados.pop()