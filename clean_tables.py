import os
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

# Excluir todos os registros das tabelas
def limpar_tabelas():
    """Exclui todos os registros das tabelas do datamart."""
    tabelas = ["Fato_Vendas", "Dim_Cliente", "Dim_Produto", "Dim_Tempo", "Dim_Vendedor"]
    conn = conectar_bd()
    if not conn:
        return
    
    cursor = conn.cursor()
    try:
        for tabela in tabelas:
            cursor.execute(f"DELETE FROM {tabela}")
            print(f"Registros excluídos da tabela {tabela}.")
        conn.commit()
    except pymssql.DatabaseError as e:
        print(f"Erro ao limpar tabelas: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    limpar_tabelas()
    print("Todas as tabelas foram limpas com sucesso.")
