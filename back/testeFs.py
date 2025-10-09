# from src.config.db.conexaoFS import getSessionFS
# from src.services.fs.fsExportService import FSExportService

# def main():
#     session = getSessionFS()
#     empresa_id = 1

#     service = FSExportService(session, empresa_id)
#     cab = service.exportarCAB(empresa_id)
#     par = service.exportarPAR(empresa_id)
#     pro = service.exportarPRO(empresa_id)
#     und = service.exportarUND(empresa_id)
#     inm = service.exportarINM(empresa_id)
#     pnm = service.exportarPNM(empresa_id)
#     nfm = service.exportarNFM(empresa_id)
#     snm = service.exportarSNM(empresa_id)
    
#     #print(cab)
#     #print("\n".join(par))
#     print("\n".join(pro))
#     #print("\n".join(und))
#     #print("\n".join(pnm))
#     #print("\n".join(inm))
#     #print("\n".join(nfm))
#     # linhas_snm = []
#     # for lista in snm.values():
#     #     linhas_snm.extend(lista)
#     # print("\n".join(linhas_snm))
    
# if __name__ == "__main__":
#     main()

# import pandas as pd
# from typing import Iterable, List, Union

# from src.config.db.conexaoFS import getSessionFS
# from src.services.fs.fsExportService import FSExportService

# headers = {
#     "CAB": [
#         "Tipo de registro",
#         "Versão do Leiaute",
#         "Sistema Origem",
#         "Data da Geração",
#         "Empresa",
#         "Data inicial dos lançamentos",
#         "Data final dos lançamentos",
#         "Comentário",
#         "Aliquotas Especificas",
#     ],
#     "PAR": [
#         "Tipo de registro",
#         "Codigo",
#         "Nome",
#         "UF",
#         "CNPJ/CPF",
#         "Inscrição Estadual",
#         "Inscrição Municipal",
#         "Informa ISS Digital",
#         "Informa DIEF",
#         "Informa DIC",
#         "Informa DEMMS",
#         "Orgação Publico",
#         "Informa Livro Eletronica",
#         "Fornecedor de Prod. Primario",
#         "Sociedade Simples",
#         "Tipo de Logadura",
#         "Logradouro",
#         "Numero",
#         "Complemento",
#         "Tipo de Bairro",
#         "Bairro",
#         "CEP",
#         "Municipio",
#         "DDD",
#         "Telefone",
#         "Suframa",
#         "Substituto ISS",
#         "Conta(Remetente/Prestador)",
#         "Conta(Destinatario/Tomador)",
#         "Pais",
#         "Exterior",
#         "Indicador do ICMS",
#         "E-mail",
#         "Hospitais",
#         "Administradora",
#         "CNAE21",
#         "CPRB",
#         "Situação Tributaria",
#         "Produtor Rural",
#         "Indicativo da Aquisição",
#     ],
#     "PRO": [
#         "Tipo de Registro",
#         "Codigo",
#         "Descrição",
#         "Codigo tuilizado Estab.",
#         "Codigo NCM",
#         "Unidade de medida padrão",
#         "Unidade Medida DIEF",
#         "Unidade Medida CENFOP",
#         "Classificação",
#         "Grupo",
#         "Genero",
#         "Codigo de barras",
#         "Redunção",
#         "Codigo GAM57",
#         "CST ICMS",
#         "CST IPI",
#         "CST COFINS",
#         "CST PIS",
#         "Codigo ANP",
#         "CST ICMS(Simples Nacional)",
#         "CSOSN",
#         "Produto Especifico",
#         "Tipo de Medicamento",
#         "Desativado",
#         "Cdoigo Indicador de Contribuição Previdenciaria",
#         "Tipo de Tributação - DIA",
#         "Codificação NVE",
#         "Indicador Especial",
#         "Codigo da Apuração",
#         "Codigo TIPI",
#         "Codigo Combustivel DIEF(PA)",
#         "Percentual de Incetivo",
#         "Prazo de Fruição",
#         "Indicador Especial de Incentivo",
#         "Percentual CSL,*",
#         "Percentual do IRPJ",
#         "Aliq. ICMS Interna",
#         "Codigos da Receita (Produto Especifico)",
#         "Cod. Recita COFINS",
#         "Cod. Receita PIS",
#         "Cod. CEST",
#         "Custo de aquisição",
#         "Substituição de ICMS",
#         "Substituição de IPI",
#         "Substintuicao de COFINS",
#         "Substituição de PIS/PASEP",
#         "Tributação Monofásica de COFINS",
#         "Tributacao do PIS/COFINS",
#         "Apuração do PIS/COFINS",
#         "Cod. Rceita Retido COFINS",
#         "Cod. Receita Retido PIS",
#         "Cod. Receita Retido CSL",
#         "Cod. Receita Retido IRPJ",
#         "Cod. Receita Retido COSIRF",
#         "Decreto 20.686/99 (AM)",
#     ],
#     "UND": [
#         "Tipo de Registro",
#         "Unidade de medida",
#         "Descrição",
#     ],
#     "INM": [
#         "Tipo registro",
#         "Valor",
#         "UF",
#         "CFOP",
#         "CFOP Transferencia",
#         "Base de Calculo ICMS",
#         "Aliquota ICMS",
#         "Valor do ICMS",
#         "Isento do ICMS",
#         "Outras do ICMS",
#         "Base de Calculo do IPI",
#         "Valor do IPI",
#         "Isentas do IPI",
#         "Outras do IPI",
#         "Substituição ICMS",
#         "Substituição IPI",
#         "Substituição COFINS",
#         "Substituição PIS/PASEP",
#         "CSTA",
#         "CSTB",
#         "Codigo da Situação tributaria do CSOSN",
#         "CSOSN",
#         "CST IPI",
#         "COFINS Monofasico",
#         "PIS Monofasico",
#         "Calcula Fecop (Decreto 29.560/08)",
#         "Aliq. Subst. (dECRETO 29.560/08)",
#         "base de calculo do FCP - Normal",
#         "Aliquota do FCP - Normal",
#         "Valor do FCP - normal",
#         "Base de Caluclo do FCP - Subst. Trib. ou Retido Ant. por Subst. Trib",
#         "Alíquota do FCP - Subst. Trib. ou Retido Ant. por Subst. Trib.",
#         "Valor do FCP - Subst. Trib. ou Retido Ant. por Subst. Trib.",
#         "Aliquota do ICMS Deferido",
#     ],
#     "SNM": [
#         "Tipo de Registro",
#         "Tipo",
#         "Custo da Aquisição",
#         "Agregacao",
#         "Base de Calculo",
#         "Aliquota",
#         "Credito de Origem",
#         "Ja recolhido",
#         "Calculo Fecop (Decreto 29.560/08)",
#     ],
# }

# def _to_rows(x: Union[str, Iterable[str]]) -> List[str]:
#     """
#     Normaliza a saída dos exportadores:
#     - Se vier string única, vira lista com 1 item.
#     - Se vier iterável (lista/tupla) de strings, normaliza cada linha.
#     Remove '|'(final) e espaços/quebras antes de fazer o split.
#     Ignora linhas vazias.
#     """
#     if isinstance(x, str):
#         x = [x]
#     rows: List[str] = []
#     for s in x:
#         if not s:
#             continue
#         s = str(s).strip()
#         if not s:
#             continue
#         # muitos builders terminam com '|'
#         s = s.rstrip("|")
#         rows.append(s)
#     return rows

# def _make_df(section: str, data: Union[str, Iterable[str]]) -> pd.DataFrame:
#     cols = headers[section]
#     rows = _to_rows(data)
#     # gera matriz já com número de colunas correto
#     matrix = []
#     for r in rows:
#         parts = r.split("|")
#         # ajusta: trunca ou completa com vazio
#         if len(parts) < len(cols):
#             parts.extend([""] * (len(cols) - len(parts)))
#         elif len(parts) > len(cols):
#             parts = parts[:len(cols)]
#         matrix.append(parts)
#     return pd.DataFrame(matrix, columns=cols)

# def main():
#     session = getSessionFS()
#     empresa_id = 1

#     service = FSExportService(session, empresa_id)

#     # Cada exportarXYZ pode retornar string única OU lista de linhas
#     cab = service.exportarCAB(empresa_id)
#     par = service.exportarPAR(empresa_id)
#     pro = service.exportarPRO(empresa_id)
#     und = service.exportarUND(empresa_id)
#     inm = service.exportarINM(empresa_id)
#     # se/quando tiver SNM, é só adicionar:
#     # snm = service.exportarSNM(empresa_id)

#     cab_df = _make_df("CAB", cab)
#     par_df = _make_df("PAR", par)
#     pro_df = _make_df("PRO", pro)
#     und_df = _make_df("UND", und)
#     inm_df = _make_df("INM", inm)
#     # snm_df = _make_df("SNM", snm)

#     with pd.ExcelWriter("Exportacao Fortes.xlsx", engine="xlsxwriter") as writer:
#         cab_df.to_excel(writer, sheet_name="CAB", index=False)
#         par_df.to_excel(writer, sheet_name="PAR", index=False)
#         pro_df.to_excel(writer, sheet_name="PRO", index=False)
#         und_df.to_excel(writer, sheet_name="UND", index=False)
#         inm_df.to_excel(writer, sheet_name="INM", index=False)
#         # snm_df.to_excel(writer, sheet_name="SNM", index=False)

#     print("Planilha Exportacao Fortes.xlsx gerada com sucesso.")

# if __name__ == "__main__":
#     main()


from src.config.db.conexaoFS import getSessionFS
from src.services.fs.fsExportService import FSExportService

def gerar_fs():
    session = getSessionFS()
    empresa_id = 1

    service = FSExportService(session, empresa_id)

    cab = service.exportarCAB(empresa_id)
    par = service.exportarPAR(empresa_id)
    pro = service.exportarPRO(empresa_id)
    und = service.exportarUND(empresa_id)
    inm = service.exportarINM(empresa_id)

    linhas = []

    # CAB pode ser string única ou lista
    if isinstance(cab, str):
        linhas.append(cab.strip())
    elif isinstance(cab, list):
        for linha in cab:
            linhas.append(linha.strip())

    for bloco in [par, pro, und, inm]:
        for linha in bloco:
            linhas.append(linha.strip())

    with open("Exportacao_Fortes.fs", "w", encoding="latin-1") as f:
        for linha in linhas:
            f.write(linha + "\n")

    print("Arquivo Exportacao_Fortes.fs gerado com sucesso.")

if __name__ == "__main__":
    gerar_fs()