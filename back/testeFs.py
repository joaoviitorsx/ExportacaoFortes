from src.config.db.conexaoFS import getSessionFS
from src.services.fs.fsExportService import FSExportService

def main():
    session = getSessionFS()
    empresa_id = 1

    service = FSExportService(session)
    cab = service.exportarCAB(empresa_id)
    par = service.exportarPAR(empresa_id)
    pro = service.exportarPRO(empresa_id)
    und = service.exportarUND(empresa_id)
    inm = service.exportarINM(empresa_id)
    pnm = service.exportarPNM(empresa_id)

    #print(cab)
    #print(par)
    #print(pro)
    #print(und)
    print("\n".join(pnm))
    #print("\n".join(inm))

if __name__ == "__main__":
    main()


# import pandas as pd
# from src.config.db.conexaoFS import getSessionFS
# from src.services.fs.fsExportService import FSExportService

# # Cole o JSON dos headers aqui
# headers_fortes_fiscal = {
#     "CAB": [
#         "Tipo de Registro", "Versao do Leiaute", "Sistema Origem", "Data da Geracao", "Empresa",
#         "Data Inicial dos Lancamentos", "Data Final dos Lancamentos", "Comentario", "Aliquotas Especificas"
#     ],
#     "PAR": [
#         "Tipo de Registro", "Codigo", "Nome", "UF", "CNPJ/CPF", "Inscricao Estadual", "Inscricao Municipal",
#         "Informa ISS Digital", "Informa DIEF", "Informa DIC", "Informa DEMMS", "Orgao Publico", "Informa Livro Eletronico",
#         "Fornecedor de Prod. Primario", "Sociedade Simples", "Tipo de Logradouro", "Logradouro", "Numero", "Complemento",
#         "Tipo de Bairro", "Bairro", "CEP", "Municipio", "DDD", "Telefone", "Suframa", "Substituto ISS",
#         "Conta (Remetente/Prestador)", "Conta (Destinatario/Tomador)", "Pais", "Exterior", "Indicador do ICMS",
#         "E-mail", "Hospitais", "Administradora", "CNAE21", "CPRB", "Situacao Tributaria", "Produtor Rural", "Indicativo da Aquisicao"
#     ],
#     "PRO": [
#         "Tipo de Registro", "Codigo", "Descricao", "Codigo Utilizado Estab.", "Codigo NCM", "Unidade de Medida Padrao",
#         "Unidade Medida DIEF", "Unidade Medida CENFOP", "Classificacao", "Grupo", "Genero", "Codigo de Barras", "Reducao",
#         "Codigo GAM57", "CST ICMS", "CST IPI", "CST COFINS", "CST PIS", "Codigo ANP", "CST ICMS (Simples Nacional)",
#         "CSOSN", "Produto Especifico", "Tipo de Medicamento", "Produto Desativado", "Codigo Indicador de Contribuicao Previdenciaria",
#         "Tipo de Tributacao - DIA", "Codificacao NVE", "Indicador Especial", "Codigo da Apuracao", "Codigo TIPI",
#         "Codigo Combustivel DIEF(PA)", "Percentual de Incentivo", "Prazo de Fruicao", "Indicador Especial de Incentivo",
#         "Percentual da CSL", "Percentual do IRPJ", "Aliq. ICMS Interna", "Codigos da Receita (Produto Especifico)",
#         "Cod. Receita COFINS", "Cod. Receita PIS", "Cod. CEST", "Custo de Aquisicao", "Substituicao de ICMS",
#         "Substituicao de IPI", "Substituicao de COFINS", "Substituicao de PIS/PASEP", "Tributacao Monofasica de COFINS",
#         "Tributacao Monofasica de PIS", "Apuracao do PIS/COFINS", "Cod. Receita Retido COFINS", "Cod. Receita Retido PIS",
#         "Cod. Receita Retido CSL", "Cod. Receita Retido IRPJ", "Cod. Receita Retido COSIRF", "Decreto 20.686/99 (AM)"
#     ],
#     "UND": [
#         "Tipo de Registro", "Unidade de Medida", "Descricao"
#     ],
#     "INM": [
#         "Tipo de Registro", "Valor", "UF", "CFOP", "CFOP Transferencia", "Base de Calculo do ICMS", "Aliquota do ICMS",
#         "Valor do ICMS", "Isentas do ICMS", "Outras do ICMS", "Base de Calculo do IPI", "Valor do IPI", "Isentas do IPI",
#         "Outras do IPI", "Substituicao ICMS", "Substituicao IPI", "Substituicao COFINS", "Substituicao PIS/PASEP",
#         "CSTA", "CSTB", "Codigo da Situacao Tributaria do CSOSN", "CSOSN", "CST IPI", "COFINS Monofasico", "PIS Monofasico",
#         "Calcula Fecop (Decreto 29.560/08)", "Aliq. Subst. (Decreto 29.560/08)", "Base de Calculo do FCP - Normal",
#         "Aliquota do FCP Normal", "Valor do FCP Normal", "Base de Calculo do FCP - Subst. Trib. ou Retido Ant. por Subst. Trib.",
#         "Aliquota do FCP - Subst. Trib. ou Retido Ant. por Subst. Trib.", "Valor do FCP Subst. Trib. ou Retido Ant. por Subst. Trib.",
#         "Aliquota do ICMS Diferimento"
#     ]
# }

# def main():
#     session = getSessionFS()
#     empresa_id = 1

#     service = FSExportService(session)
#     cab = service.exportarCAB(empresa_id)
#     par = service.exportarPAR(empresa_id)
#     pro = service.exportarPRO(empresa_id)
#     und = service.exportarUND(empresa_id)
#     inm = service.exportarINM(empresa_id)

#     # Transformar cada dado em DataFrame usando os headers do JSON
#     df_cab = pd.DataFrame([cab.split("|")], columns=headers_fortes_fiscal["CAB"])
#     df_par = pd.DataFrame([linha.split("|") for linha in par], columns=headers_fortes_fiscal["PAR"])
#     df_pro = pd.DataFrame([linha.split("|") for linha in pro], columns=headers_fortes_fiscal["PRO"])
#     df_und = pd.DataFrame([linha.split("|") for linha in und], columns=headers_fortes_fiscal["UND"])
#     df_inm = pd.DataFrame([linha.split("|") for linha in inm], columns=headers_fortes_fiscal["INM"])

#     # Gerar planilha Excel com abas
#     with pd.ExcelWriter("fs_export.xlsx", engine="xlsxwriter") as writer:
#         df_cab.to_excel(writer, sheet_name="CAB", index=False)
#         df_par.to_excel(writer, sheet_name="PAR", index=False)
#         df_pro.to_excel(writer, sheet_name="PRO", index=False)
#         df_und.to_excel(writer, sheet_name="UND", index=False)
#         df_inm.to_excel(writer, sheet_name="INM", index=False)

#     print("Planilha fs_export.xlsx gerada com sucesso.")

# if __name__ == "__main__":
#     main()