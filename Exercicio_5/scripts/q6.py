import ast
import os

import pandas as pd
from scipy.stats import chi2_contingency
from sklearn.feature_selection import chi2

DATA_PATH = os.path.join("..", "data", "transacoes_bancarias.csv")

DIAS = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo",
}
ORDEM_DIAS = [
    "domingo",
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
]


def minmax_grupo(serie):
    minimo = serie.min()
    maximo = serie.max()
    if maximo == minimo:
        return pd.Series(0.0, index=serie.index)
    return (serie - minimo) / (maximo - minimo)


df = pd.read_csv(DATA_PATH)
df["Data"] = pd.to_datetime(df["Data"])

estado = df["Estado"].apply(ast.literal_eval)
df["UF"] = estado.apply(lambda par: par[0])
df["Estado_nome"] = estado.apply(lambda par: par[1])

# --- Sexo e tipo de produto: one-hot + qui-quadrado e correlação ---
produto = pd.get_dummies(df["Produto"], dtype=int)
sexo = (df["Sexo"] == "Feminino").astype(int)

qui_prod, p_prod = chi2(produto, sexo)
correlacao = produto.apply(lambda coluna: coluna.corr(sexo))

contagem = pd.crosstab(df["Produto"], df["Sexo"])
associacao = pd.DataFrame({
    "produto": produto.columns,
    "n_feminino": contagem["Feminino"].reindex(produto.columns).to_numpy(),
    "n_masculino": contagem["Masculino"].reindex(produto.columns).to_numpy(),
    "correlacao": correlacao.to_numpy(),
    "chi2": qui_prod,
    "p_valor": p_prod,
})
associacao = associacao.sort_values("correlacao", key=lambda s: s.abs(), ascending=False)

tabela = pd.crosstab(df["Sexo"], df["Produto"])
qui2, p_global, gl, _ = chi2_contingency(tabela)
n = int(tabela.to_numpy().sum())
linhas, colunas = tabela.shape
cramer = (qui2 / (n * (min(linhas, colunas) - 1))) ** 0.5

global_df = pd.DataFrame({
    "chi2": [qui2],
    "p_valor": [p_global],
    "graus_liberdade": [gl],
    "cramer_v": [cramer],
    "n": [n],
})

print("Associação global Sexo x Produto:")
print(global_df.to_string(index=False))
print("\nAssociação por produto (Sexo Feminino = 1):")
print(associacao.to_string(index=False))

# --- Dia da semana com mais compras ---
df["dia_semana"] = df["Data"].dt.day_of_week.map(DIAS)
contagem_dias = df["dia_semana"].value_counts().reindex(ORDEM_DIAS)
dias_df = contagem_dias.rename("compras").reset_index()
dias_df.columns = ["dia_semana", "compras"]
dias_df["proporcao"] = dias_df["compras"] / dias_df["compras"].sum()

dia_topo = dias_df.loc[dias_df["compras"].idxmax()]
print("\nCompras por dia da semana:")
print(dias_df.to_string(index=False))
print(f"\nDia com mais compras: {dia_topo['dia_semana']} ({int(dia_topo['compras'])})")

# --- Valor na escala 0 a 1 dentro de cada estado ---
df["Valor_norm"] = df.groupby("UF")["Valor"].transform(minmax_grupo)

resumo_estado = (
    df.groupby(["UF", "Estado_nome"], as_index=False)
    .agg(
        n=("Valor", "size"),
        valor_min=("Valor", "min"),
        valor_max=("Valor", "max"),
        norm_min=("Valor_norm", "min"),
        norm_max=("Valor_norm", "max"),
    )
    .sort_values("UF")
)

print("\nMin-Max do valor por estado:")
print(resumo_estado.to_string(index=False))
print(
    "\nEstados com norm_min = 0 e norm_max = 1:",
    int(((resumo_estado["norm_min"] == 0) & (resumo_estado["norm_max"] == 1)).sum()),
    "de",
    len(resumo_estado),
)

amostra = df[["Data", "Produto", "UF", "Estado_nome", "Valor", "Valor_norm"]].copy()
amostra["Data"] = amostra["Data"].dt.strftime("%Y-%m-%d %H:%M:%S")

os.makedirs("results", exist_ok=True)
associacao.to_csv("results/q6_sexo_produto.csv", index=False, encoding="utf-8-sig")
global_df.to_csv("results/q6_sexo_produto_global.csv", index=False, encoding="utf-8-sig")
dias_df.to_csv("results/q6_dia_semana.csv", index=False, encoding="utf-8-sig")
resumo_estado.to_csv("results/q6_valor_estado.csv", index=False, encoding="utf-8-sig")
amostra.to_csv("results/q6_valor_norm.csv", index=False, encoding="utf-8-sig")
