import pandas as pd
from ...utils.aliquota import categoriaAliquota, validarAliquota

class ValidacaoTransferService:
    def __init__(self):
        self.erros = []

    def validar(self, df: pd.DataFrame) -> pd.DataFrame:
        self.erros = []

        # 1. Código
        codigoInvalidos = df[df["codigo"].isna() | (df["codigo"].str.strip() == "")]
        if not codigoInvalidos.empty:
            self.erros.append(f"Códigos inválidos: {len(codigoInvalidos)}")

        # 2. Produto
        produtosInvalidos = df[df["produto"].isna() | (df["produto"].str.strip() == "")]
        if not produtosInvalidos.empty:
            self.erros.append(f"Produtos inválidos: {len(produtosInvalidos)}")

        # 3. NCM → obrigatório e apenas dígitos
        ncmInvalidos = df[df["ncm"].isna() | (~df["ncm"].astype(str).str.match(r"^\d+$"))]
        if not ncmInvalidos.empty:
            self.erros.append(f"NCM inválidos: {len(ncmInvalidos)}")

        # 4. Alíquota
        aliquotasInvalidas = df[~df["aliquota"].apply(validarAliquota)]
        if not aliquotasInvalidas.empty:
            self.erros.append(f"Alíquotas inválidas: {len(aliquotasInvalidas)}")

        # 5. Categoria Fiscal → preencher se vazia
        df["categoriaFiscal"] = df.apply(
            lambda row: row["categoriaFiscal"]
            if pd.notna(row["categoriaFiscal"]) and str(row["categoriaFiscal"]).strip() != ""
            else categoriaAliquota(row["aliquota"]),
            axis=1
        )

        if self.erros:
            print("[ERRO] Validação falhou:")
            for e in self.erros:
                print("   -", e)

            return df.drop(codigoInvalidos.index).drop(produtosInvalidos.index).drop(ncmInvalidos.index).drop(aliquotasInvalidas.index)
                             
        else:
            print("[INFO] Validação concluída sem erros.")

        return df
