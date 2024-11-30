import sqlite3

# Conectando ao banco de dados (ou criando um novo se não existir)
database_path = 'data/database.db'  # Atualize o caminho se necessário
conn = sqlite3.connect(database_path)
cursor = conn.cursor()
# Criando a tabela categorias_eventos se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias_eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT UNIQUE NOT NULL
)
''')

# Inserindo as categorias na tabela
categorias = ['olimpíada', 'futebol', 'eleições', 'bolsa de valores']

for categoria in categorias:
    try:
        cursor.execute('INSERT INTO categorias_eventos (nome) VALUES (?)', (categoria,))
    except sqlite3.IntegrityError:
        print(f"A categoria '{categoria}' já existe e não será inserida novamente.")

# Salvando as mudanças e fechando a conexão
conn.commit()
conn.close()

print("Categorias inseridas com sucesso.")
