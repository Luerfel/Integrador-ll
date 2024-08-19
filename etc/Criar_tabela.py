import os
import sqlite3

# Caminho do banco de dados
db_path = os.path.join('data', 'database.db')

def criar_tabelas():
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Conectar ao banco de dados (ou criar, se não existir)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Criar as tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        data_nascimento DATE NOT NULL,
        tipo TEXT NOT NULL DEFAULT 'usuario',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor_cota REAL NOT NULL CHECK (valor_cota >= 1.00),
        data_evento DATE NOT NULL,
        periodo_apostas TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pendente',
        id_criador INTEGER NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_criador) REFERENCES usuarios(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias_eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos_categorias (
        id_evento INTEGER NOT NULL,
        id_categoria INTEGER NOT NULL,
        PRIMARY KEY (id_evento, id_categoria),
        FOREIGN KEY (id_evento) REFERENCES eventos(id) ON DELETE CASCADE,
        FOREIGN KEY (id_categoria) REFERENCES categorias_eventos(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carteiras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        saldo REAL NOT NULL DEFAULT 0.00,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_carteira INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        valor REAL NOT NULL,
        data_transacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        detalhes TEXT,
        FOREIGN KEY (id_carteira) REFERENCES carteiras(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS apostas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_evento INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        valor REAL NOT NULL CHECK (valor >= 1.00),
        opcao TEXT NOT NULL,
        data_aposta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_evento) REFERENCES eventos(id) ON DELETE CASCADE,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados_eventos (
        id_evento INTEGER PRIMARY KEY,
        resultado TEXT NOT NULL,
        data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_evento) REFERENCES eventos(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS moderacoes_eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_evento INTEGER NOT NULL,
        id_moderador INTEGER NOT NULL,
        acao TEXT NOT NULL,
        motivo_rejeicao TEXT,
        data_moderacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_evento) REFERENCES eventos(id) ON DELETE CASCADE,
        FOREIGN KEY (id_moderador) REFERENCES usuarios(id) ON DELETE CASCADE
    )
    ''')

    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso.")

def inserir_moderador(nome, email, senha, data_nascimento):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO usuarios (nome, email, senha, data_nascimento, tipo)
    VALUES (?, ?, ?, ?, 'moderador')
    ''', (nome, email, senha, data_nascimento))
    conn.commit()
    conn.close()
    print("Moderador inserido com sucesso.")

def listar_tabelas():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    conn.close()
    if tabelas:
        print("Tabelas no banco de dados:")
        for tabela in tabelas:
            print(tabela[0])
    else:
        print("Nenhuma tabela encontrada.")

def menu():
    while True:
        print("\nMenu:")
        print("1. Criar Tabelas")
        print("2. Inserir Moderador")
        print("3. Listar Tabelas")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            criar_tabelas()
        elif escolha == '2':
            nome = input("Nome do Moderador: ")
            email = input("Email do Moderador: ")
            senha = input("Senha do Moderador: ")
            data_nascimento = input("Data de Nascimento (YYYY-MM-DD): ")
            inserir_moderador(nome, email, senha, data_nascimento)
        elif escolha == '3':
            listar_tabelas()
        elif escolha == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu()
