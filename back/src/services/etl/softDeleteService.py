import re
from sqlalchemy import text


class SoftDeleteService:

    @staticmethod
    def softDelete(session, empresa_id: int):
        tabelas = [
            "registro_0000",
            "registro_0150",
            "registro_0200",
            "registro_c100",
            "registro_c170",
            "registro_c190",
        ]

        total_desativados = 0
        for tabela in tabelas:
            sql = text(f"""
                UPDATE {tabela}
                SET ativo = 0
                WHERE empresa_id = :empresa_id AND ativo = 1
            """)
            resultado = session.execute(sql, {"empresa_id": empresa_id})
            total_desativados += resultado.rowcount or 0

        session.commit()
        session.close()
        return total_desativados

    @staticmethod
    def extrairPeriodo(arquivos: list[str]) -> str | None:
        if not arquivos:
            return None

        periodos_encontrados = set()
        encodings = ["latin-1", "utf-8", "utf-16", "cp1252"]

        for caminho in arquivos:
            for enc in encodings:
                try:
                    with open(caminho, "r", encoding=enc, errors="ignore") as f:
                        primeira_linha = f.readline().strip()
                        if primeira_linha.startswith("|0000|"):
                            partes = primeira_linha.split("|")
                            if len(partes) > 4:
                                data_ini = partes[4]
                                if re.match(r"\d{8}", data_ini):
                                    mes = data_ini[2:4]
                                    ano = data_ini[4:]
                                    periodos_encontrados.add(f"{mes}/{ano}")
                                    break
                except Exception:
                    continue

        if not periodos_encontrados:
            return None

        if len(periodos_encontrados) > 1:
            return sorted(periodos_encontrados, reverse=True)[0]

        return periodos_encontrados.pop()
