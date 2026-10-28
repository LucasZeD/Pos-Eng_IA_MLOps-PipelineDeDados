import os

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

data = {
    "Nota_Matemática": [8, 7, 9, 6, 8],
    "Nota_Português": [7, 6, 8, 5, 7],
    "Satisfação_Curso": [4, 3, 5, 2, 4],
}

df = pd.DataFrame(data)
print("Notas e satisfação originais:")
print(df.to_string(index=False))

# grau 2: quadrados e produtos entre as colunas, sem o termo constante
poly = PolynomialFeatures(degree=2, include_bias=False)
transformado = poly.fit_transform(df)
nomes = poly.get_feature_names_out(df.columns)
df_poly = pd.DataFrame(transformado, columns=nomes)

print("\nFeatures polinomiais (grau 2):")
print(df_poly.to_string(index=False))

os.makedirs("results", exist_ok=True)
df_poly.to_csv("results/q4_polynomial.csv", index=False, encoding="utf-8-sig")
