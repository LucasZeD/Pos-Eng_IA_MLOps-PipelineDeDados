import os

import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

data = {
    "Matemática": [85, 92, 78, 96, 88],
    "Português": [7, 5, 8, 9, 6],
}

df = pd.DataFrame(data)
print("Notas originais:")
print(df.to_string(index=False))

# Min-Max: (x - xmin) / (xmax - xmin), intervalo [0, 1]
scaler_mm = MinMaxScaler()
minmax = pd.DataFrame(
    scaler_mm.fit_transform(df),
    columns=["Matemática_minmax", "Português_minmax"],
)

# Z-score: (x - média) / desvio, com desvio populacional (StandardScaler)
scaler_z = StandardScaler()
zscore = pd.DataFrame(
    scaler_z.fit_transform(df),
    columns=["Matemática_zscore", "Português_zscore"],
)

resultado = pd.concat([df, minmax, zscore], axis=1)

parametros = pd.DataFrame({
    "variavel": df.columns,
    "min": scaler_mm.data_min_,
    "max": scaler_mm.data_max_,
    "media": scaler_z.mean_,
    "desvio": scaler_z.scale_,
})

print("\nParâmetros usados nas fórmulas:")
print(parametros.to_string(index=False))

print("\nNotas normalizadas (Min-Max) e padronizadas (Z-score):")
print(resultado.to_string(index=False))

os.makedirs("results", exist_ok=True)
resultado.to_csv("results/q3_escalas.csv", index=False, encoding="utf-8-sig")
parametros.to_csv("results/q3_parametros.csv", index=False, encoding="utf-8-sig")
