import pandas as pd
import os

data = {
    'Produto': [
        'Eletrônicos',
        'Roupas',
        'Eletrodomésticos',
        'Eletrônicos',
        'Livros',
        'Roupas',
        'Livros'
    ]
}

df = pd.DataFrame(data)
print("Raw df:")
print(df)

# identifica valores distintos de uma var categórica e cria uma coluna para cada categoria.
print("\nOne-hot encoded df:")
df_encoded = pd.get_dummies(df, columns=['Produto'], dtype=int)
print(df_encoded)

os.makedirs("results", exist_ok=True)
df_encoded.to_csv("results/q1.csv", index=False, sep=";", encoding="utf-8-sig")
