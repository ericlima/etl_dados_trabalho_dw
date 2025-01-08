import pandas as pd
import numpy as np

# Configurações gerais
num_clientes = 100
num_produtos = 50
num_vendedores = 20
num_dias = (365 * 5) + 2
num_vendas = 5000

# Geração da Dimensão Cliente
clientes = {
    "ID_Cliente": np.arange(1, num_clientes + 1),
    "Nome_Cliente": [f"Cliente_{i}" for i in range(1, num_clientes + 1)],
    "Data_Nascimento": pd.date_range(start="1970-01-01", periods=num_clientes, freq="M"),
    "Genero": np.random.choice(["M", "F"], size=num_clientes),
    "Categoria_Cliente": np.random.choice(["Regular", "VIP"], size=num_clientes),
    "Cidade": np.random.choice(["Lisboa", "Porto", "Castelo Branco", "Fátima"], size=num_clientes),
    "Pais": ["Portugal"] * num_clientes
}
df_clientes = pd.DataFrame(clientes)

# Geração da Dimensão Produto
produtos = {
    "ID_Produto": np.arange(1, num_produtos + 1),
    "Nome_Produto": [f"Produto_{i}" for i in range(1, num_produtos + 1)],
    "Categoria_Produto": np.random.choice(["Eletrônicos", "Roupas", "Alimentos"], size=num_produtos),
    "Subcategoria_Produto": np.random.choice(["Premium", "Básico"], size=num_produtos),
    "Marca": [f"Marca_{i}" for i in range(1, num_produtos + 1)],
    "Preco_Unitario": np.random.uniform(10.0, 1000.0, num_produtos).round(2),
    "Data_Lancamento": pd.date_range(start="2020-01-01", periods=num_produtos, freq="M")
}
df_produtos = pd.DataFrame(produtos)

# Geração da Dimensão Tempo
data_calculada = pd.date_range(start="2020-01-01", periods=num_dias, freq="D")
tempo = {
    "ID_Tempo": np.arange(1, num_dias + 1),
    "Data": data_calculada,
    "Dia": data_calculada.day,
    "Mes": data_calculada.month,
    "Ano": data_calculada.year,
    "Trimestre": data_calculada.quarter,
     "Semana": data_calculada.isocalendar().week.astype(int)
}
df_tempo = pd.DataFrame(tempo)

# Geração da Dimensão Vendedor
vendedores = {
    "ID_Vendedor": np.arange(1, num_vendedores + 1),
    "Nome_Vendedor": [f"Vendedor_{i}" for i in range(1, num_vendedores + 1)],
    "Regiao": np.random.choice(["Sul", "Sudeste", "Nordeste"], size=num_vendedores),
    "Data_Contratacao": pd.date_range(start="2015-01-01", periods=num_vendedores, freq="Y")
}
df_vendedores = pd.DataFrame(vendedores)

# Geração da Fato Vendas
vendas = {
    "ID_Venda": np.arange(1, num_vendas + 1),
    "ID_Cliente": np.random.choice(df_clientes["ID_Cliente"], size=num_vendas),
    "ID_Produto": np.random.choice(df_produtos["ID_Produto"], size=num_vendas),
    "ID_Tempo": np.random.choice(df_tempo["ID_Tempo"], size=num_vendas),
    "ID_Vendedor": np.random.choice(df_vendedores["ID_Vendedor"], size=num_vendas),
    "Quantidade": np.random.randint(1, 10, num_vendas),
    "Valor_Unitario": np.random.uniform(10.0, 1000.0, num_vendas).round(2),
    "Desconto": np.random.uniform(0.0, 50.0, num_vendas).round(2),
    "Metodo_Pagamento": np.random.choice(["Cartão de Crédito", "Paypal", "MBWay", "Dinheiro"], size=num_vendas),
    "Status_Venda": np.random.choice(["Concluída", "Pendente", "Cancelada"], size=num_vendas)
}
df_vendas = pd.DataFrame(vendas)
df_vendas["Valor_Total"] = (df_vendas["Quantidade"] * df_vendas["Valor_Unitario"]).round(2)
df_vendas["Receita_Liquida"] = (df_vendas["Valor_Total"] - df_vendas["Desconto"]).round(2)

# Salvando os dados em arquivos CSV (opcional)
df_clientes.to_csv("Dim_Cliente.csv", index=False)
df_produtos.to_csv("Dim_Produto.csv", index=False)
df_tempo.to_csv("Dim_Tempo.csv", index=False)
df_vendedores.to_csv("Dim_Vendedor.csv", index=False)
df_vendas.to_csv("Fato_Vendas.csv", index=False)

# Exibindo os primeiros registros de cada tabela
print("Clientes:\n", df_clientes.head())
print("Produtos:\n", df_produtos.head())
print("Tempo:\n", df_tempo.head())
print("Vendedores:\n", df_vendedores.head())
print("Vendas:\n", df_vendas.head())
