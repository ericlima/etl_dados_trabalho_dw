import os
import pandas as pd
from dotenv import load_dotenv
import pymssql

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def conectar_bd():
    """Conecta ao banco de dados usando as configurações do arquivo .env."""
    server = os.getenv("DB_SERVER")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    
    try:
        conn = pymssql.connect(server, user, password, database)
        return conn
    except pymssql.InterfaceError as e:
        print(f"Erro de conexão: {e}")
        return None

# Função para carregar CSV e inserir dados no banco de dados
def carregar_dados(tabela, arquivo_csv, colunas_excluir=None):
    """
    Carrega os dados de um arquivo CSV e insere na tabela do banco de dados.

    :param tabela: Nome da tabela no banco de dados.
    :param arquivo_csv: Caminho do arquivo CSV.
    :param colunas_excluir: Lista de colunas a serem excluídas do insert.
    """
    conn = conectar_bd()
    if not conn:
        return
    
    cursor = conn.cursor()

    try:
        # Habilitar inserção em colunas identity
        cursor.execute(f"SET IDENTITY_INSERT {tabela} ON")

        # Carregar dados do CSV
        df = pd.read_csv(arquivo_csv)

        # Remover colunas calculadas
        if colunas_excluir:
            df = df.drop(columns=colunas_excluir, errors='ignore')

        # Gerar a string de inserção dinâmica
        colunas = ", ".join(df.columns)
        valores = ", ".join(["%s"] * len(df.columns))
        query = f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})"

        # Inserir dados linha a linha
        for _, row in df.iterrows():
            cursor.execute(query, tuple(row))

        conn.commit()
        print(f"Dados inseridos na tabela {tabela} com sucesso.")

        # Desabilitar inserção em colunas identity
        cursor.execute(f"SET IDENTITY_INSERT {tabela} OFF")
    except Exception as e:
        print(f"Erro ao inserir dados na tabela {tabela}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Exemplo de carga para cada tabela
    carregar_dados("Dim_Cliente", "Dim_Cliente.csv")
    carregar_dados("Dim_Produto", "Dim_Produto.csv")
    carregar_dados("Dim_Tempo", "Dim_Tempo.csv")
    carregar_dados("Dim_Vendedor", "Dim_Vendedor.csv")
    carregar_dados("Fato_Vendas", "Fato_Vendas.csv", colunas_excluir=["Valor_Total", "Receita_Liquida"])
