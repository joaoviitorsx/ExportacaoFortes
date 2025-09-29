# from src.config.db.conexaoFS import getSessionFS
# from src.services.fs.fsExportService import FSExportService

# def main():
#     session = getSessionFS()
#     empresa_id = 1

#     service = FSExportService(session)
#     cab = service.exportarCAB(empresa_id)
#     par = service.exportarPAR(empresa_id)
#     pro = service.exportarPRO(empresa_id)
#     und = service.exportarUND(empresa_id)
#     inm = service.exportarINM(empresa_id)
#     pnm = service.exportarPNM(empresa_id)
#     nfm = service.exportarNFM(empresa_id)
#     snm = service.exportarSNM(empresa_id)

#     print("\n".join(cab))
#     print("\n".join(par))
#     print("\n".join(pro))
#     print("\n".join(und))
#     print("\n".join(pnm))
#     print("\n".join(inm))
#     print("\n".join(nfm))
#     print("\n".join(snm))
    
    

# if __name__ == "__main__":
#     main()


# import pandas as pd
# from src.config.db.conexaoFS import getSessionFS
# from src.services.fs.fsExportService import FSExportService

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
#     "UND": [
#         "Tipo de Registro", "Unidade de Medida", "Descricao"
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
#     "NFM": [
#         "Tipo de Registro", "Codigo do Documento", "Tipo de Operacao", "Modelo do Documento", "Especie do Documento",
#         "Participante", "Serie do Documento", "Subserie", "Numero do Documento", "Numero Final", "Data de Emissao",
#         "Data de Entrada/Saida", "Hora", "Tipo de Conhecimento de Frete", "Consumo", "Natureza da Operacao",
#         "Natureza da Operacao (Suframa)", "Cupom Fiscal Vinculado", "Cancelado", "Situacao do Documento", "Valor Total do Documento",
#         "Desconto", "Valor do Desconto", "Valor das Mercadorias", "Frete Pago/A Pagar", "Valor do Frete", "Valor do Seguro",
#         "Outras Despesas", "Base de Calculo do ICMS", "Valor do ICMS", "Base de Calculo do ICMS ST", "Valor do ICMS ST",
#         "Valor do IPI", "Valor do PIS", "Valor da COFINS", "Reservado_36", "Reservado_37", "Calcula Credito", "Reservado_39",
#         "Tipo de Documento", "Reservado_41", "Reservado_42", "Contabil", "Reservado_44", "Chave Eletronica", "Informacoes Complementares",
#         "Reservado_47", "Reservado_48", "Reservado_49", "Reservado_50", "Reservado_51", "Reservado_52", "Reservado_53", "Reservado_54",
#         "Reservado_55", "Reservado_56", "Reservado_57", "Reservado_58", "Reservado_59", "Reservado_60", "Reservado_61", "Tipo de Frete",
#         "Reservado_63", "Reservado_64", "Reservado_65", "Reservado_66", "Reservado_67", "Reservado_68", "Reservado_69", "Reservado_70",
#         "Reservado_71", "Reservado_72", "Reservado_73", "Reservado_74", "Reservado_75", "Reservado_76", "Reservado_77", "Reservado_78",
#         "Reservado_79"
#     ],
#     "PNM": [
#         "Tipo de Registro", "Codigo do Produto", "CFOP", "CFOP Transferencia", "CSTA", "CSTB", "Unidade", "Quantidade",
#         "Valor Bruto", "Valor do Desconto", "Tributacao ICMS", "Base de Calculo ICMS", "Aliquota ICMS", "Base de Calculo ICMS ST",
#         "Percentual Reducao Base ICMS ST", "Aliquota ICMS ST", "Reservado_17", "Reservado_18", "Reservado_19", "Valor ICMS ST",
#         "Reservado_21", "Valor ICMS", "Percentual Reducao Base ICMS", "Reservado_24", "Reservado_25", "Reservado_26",
#         "Reservado_27", "Reservado_28", "Reservado_29", "Reservado_30", "Reservado_31", "Tipo Tributacao IPI", "Base de Calculo IPI",
#         "Aliquota IPI", "Valor IPI", "CST IPI", "CST COFINS", "CST PIS", "Base de Calculo COFINS", "Base de Calculo PIS",
#         "Valor do Frete", "Valor do Seguro", "Reservado_43", "Valor Total", "Natureza Receita COFINS", "Natureza Receita PIS",
#         "Reservado_47", "Reservado_48", "CSOSN Origem", "CSOSN Codigo", "Tipo Calculo COFINS", "Aliquota COFINS %", "Aliquota COFINS R$",
#         "Valor COFINS", "Tipo Calculo PIS", "Aliquota PIS %", "Aliquota PIS R$", "Valor PIS", "Codigo Ajuste Fiscal", "Reservado_60",
#         "Reservado_61", "Outras Despesas", "Codigo Contabil", "Reservado_64", "NCM", "Reservado_66", "Reservado_67", "Reservado_68",
#         "Reservado_69", "Reservado_70", "Reservado_71", "Reservado_72", "Reservado_73", "Reservado_74", "Reservado_75", "Reservado_76",
#         "Reservado_77", "Reservado_78", "Reservado_79", "Reservado_80", "Reservado_81", "Reservado_82", "Reservado_83", "Reservado_84",
#         "Reservado_85", "Reservado_86", "Reservado_87", "Reservado_88", "Reservado_89", "Reservado_90", "Reservado_91", "Reservado_92",
#         "Reservado_93", "Reservado_94", "Reservado_95", "Reservado_96", "Reservado_97", "Reservado_98", "Reservado_99", "Reservado_100",
#         "Reservado_101", "Reservado_102", "Reservado_103", "Reservado_104", "Reservado_105", "Reservado_106", "Reservado_107",
#         "Reservado_108", "Reservado_109", "Reservado_110", "Reservado_111", "Reservado_112", "Reservado_113", "Reservado_114",
#         "Codigo CEST", "Reservado_116", "Reservado_117", "Reservado_118", "Reservado_119", "Reservado_120", "Reservado_121"
#     ],
#     "SNM": [
#         "Tipo de Registro", "Codigo do Documento", "CFOP", "CSTA", "CSTB", "Aliquota do ICMS", "Valor Contabil",
#         "Base de Calculo do ICMS", "Valor do ICMS", "Valor de Isentas", "Valor de Outras", "Base de Calculo do ICMS ST",
#         "Valor do ICMS ST", "Valor do IPI"
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
#     ],
# }

# def main():
#     session = getSessionFS()
#     empresa_id = 1

#     service = FSExportService(session)
#     cab = service.exportarCAB(empresa_id)
#     par = service.exportarPAR(empresa_id)
#     und = service.exportarUND(empresa_id)
#     pro = service.exportarPRO(empresa_id)
#     nfm = service.exportarNFM(empresa_id)
#     pnm = service.exportarPNM(empresa_id)
#     snm = service.exportarSNM(empresa_id)
#     inm = service.exportarINM(empresa_id)

#     # Transformar cada dado em DataFrame usando os headers do JSON
#     df_cab = pd.DataFrame([cab.split("|")], columns=headers_fortes_fiscal["CAB"])
#     df_par = pd.DataFrame([linha.split("|") for linha in par], columns=headers_fortes_fiscal["PAR"])
#     df_und = pd.DataFrame([linha.split("|") for linha in und], columns=headers_fortes_fiscal["UND"])
#     df_pro = pd.DataFrame([linha.split("|") for linha in pro], columns=headers_fortes_fiscal["PRO"])
#     df_nfm = pd.DataFrame([linha.split("|") for linha in nfm], columns=headers_fortes_fiscal["NFM"])
#     df_pnm = pd.DataFrame([linha.split("|") for linha in pnm], columns=headers_fortes_fiscal["PNM"])
#     df_snm = pd.DataFrame([linha.split("|") for linha in snm], columns=headers_fortes_fiscal["SNM"])
#     df_inm = pd.DataFrame([linha.split("|") for linha in inm], columns=headers_fortes_fiscal["INM"])

#     with pd.ExcelWriter("Exportacao Fortes.xlsx", engine="xlsxwriter") as writer:
#         df_cab.to_excel(writer, sheet_name="CAB", index=False)
#         df_par.to_excel(writer, sheet_name="PAR", index=False)
#         df_und.to_excel(writer, sheet_name="UND", index=False)
#         df_pro.to_excel(writer, sheet_name="PRO", index=False)
#         df_nfm.to_excel(writer, sheet_name="NFM", index=False)
#         df_pnm.to_excel(writer, sheet_name="PNM", index=False)
#         df_snm.to_excel(writer, sheet_name="SNM", index=False)
#         df_inm.to_excel(writer, sheet_name="INM", index=False)

#     print("Planilha Exportacao Fortes.xlsx gerada com sucesso.")

# if __name__ == "__main__":
#     main()


from src.config.db.conexaoFS import getSessionFS
from src.services.fs.fsExportService import FSExportService
from src.services.fs.TRA.builderTRA import builderTRA

def gerar_fs():
    session = getSessionFS()
    empresa_id = 1

    service = FSExportService(session)

    # montar todas as linhas do arquivo (sem TRA ainda)
    linhas = []
    cab = service.exportarCAB(empresa_id)              # string única
    par = service.exportarPAR(empresa_id)              # lista de linhas
    und = service.exportarUND(empresa_id)
    pro = service.exportarPRO(empresa_id)
    nfm = service.exportarNFM(empresa_id)
    pnm = service.exportarPNM(empresa_id)
    snm = service.exportarSNM(empresa_id)
    inm = service.exportarINM(empresa_id)

    linhas.append(cab)
    linhas.extend(par)
    linhas.extend(und)
    linhas.extend(pro)
    linhas.extend(nfm)
    linhas.extend(pnm)
    linhas.extend(snm)
    linhas.extend(inm)

    # agora sim, conta tudo e soma +1 para o TRA
    quantidade_total = len(linhas) + 1
    tra = builderTRA(quantidade_total)
    linhas.append(tra)

    # salvar em arquivo .fs
    with open("Exportacao_Fortes.fs", "w", encoding="latin-1") as f:
        for linha in linhas:
            f.write(linha.strip() + "\n")

    print("Arquivo Exportacao_Fortes.fs gerado com sucesso.")


if __name__ == "__main__":
    gerar_fs()
