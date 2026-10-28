import os

import pandas as pd

data = {
    "Idade": [28, 35, 45, 22, 31],
    "Produtos_Comprados": [5, 9, 7, 3, 6],
}

df = pd.DataFrame(data)

# feature de interação: a aula lista esse produto entre as transformações lineares
df["Idade_x_Produtos"] = df["Idade"] * df["Produtos_Comprados"]

correlacao = df["Idade"].corr(df["Produtos_Comprados"])

print("Features com a interação linear:")
print(df.to_string(index=False))
print(f"\nCorrelação de Pearson (Idade, Produtos_Comprados): {correlacao:.6f}")

resumo = pd.DataFrame({
    "par": ["Idade x Produtos_Comprados"],
    "pearson": [correlacao],
})

os.makedirs("results", exist_ok=True)
df.to_csv("results/q5_interacao.csv", index=False, encoding="utf-8-sig")
resumo.to_csv("results/q5_correlacao.csv", index=False, encoding="utf-8-sig")
