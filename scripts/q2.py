import os
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression

data = {
    'Tamanho': [150, 120, 180, 130, 160],
    'Quartos': [3, 2, 4, 3, 4],
    'Preço': [200000, 180000, 250000, 190000, 220000],
    'Localização': ['Norte', 'Leste', 'Oeste', 'Sul', 'Centro']
}

df = pd.DataFrame(data)

# separating target from parameters
x = df.drop(columns="Preço")
y = df["Preço"]

# encoding categorical data
x = pd.get_dummies(x, columns=["Localização"], dtype=int)

# selecting top 2 features by value
selector = SelectKBest(score_func=f_regression, k=2)
selector.fit(x, y)

results = pd.DataFrame({
    "feature": x.columns,
    "f_value": selector.scores_,
    "p_value": selector.pvalues_,
    "selected": selector.get_support()
})

# sort by value
results = results.sort_values("f_value", ascending=False)

# export
os.makedirs("results", exist_ok=True)
results.to_csv("results/q2_feature_rank.csv", index=False, encoding="utf-8-sig")

selected_feats = x.loc[:, selector.get_support()]
selected_feats.to_csv("results/q2_feature_selection.csv", index=False, encoding="utf-8-sig")

print("\nFeature ranking:")
print(results.to_string(index=False))

print("\nSelected features:")
print(selected_feats.columns.tolist())
