import sqlite3

def criar_tabelas():
    # Conectar ao banco de dados (ou criar, se não existir)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Criar tabela usuarios
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

    # Criar tabela eventos
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

    # Criar tabela categorias_eventos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias_eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
    ''')

    # Criar tabela eventos_categorias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS eventos_categorias (
        id_evento INTEGER NOT NULL,
        id_categoria INTEGER NOT NULL,
        PRIMARY KEY (id_evento, id_categoria),
        FOREIGN KEY (id_evento) REFERENCES eventos(id) ON DELETE CASCADE,
        FOREIGN KEY (id_categoria) REFERENCES categorias_eventos(id) ON DELETE CASCADE
    )
    ''')

    # Criar tabela carteiras
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carteiras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER NOT NULL,
        saldo REAL NOT NULL DEFAULT 0.00,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
    )
    ''')

    # Criar tabela transacoes
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

    # Criar tabela apostas
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

    # Criar tabela resultados_eventos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados_eventos (
        id_evento INTEGER PRIMARY KEY,
        resultado TEXT NOT NULL,
        data_processamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_evento) REFERENCES eventos(id) ON DELETE CASCADE
    )
    ''')

    # Criar tabela moderacoes_eventos
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

    # Confirmar as alterações
    conn.commit()

    # Fechar a conexão
    conn.close()

def inserir_moderador(nome, email, senha, data_nascimento):
    # Conectar ao banco de dados
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Inserir novo moderador na tabela usuarios
    cursor.execute('''
    INSERT INTO usuarios (nome, email, senha, data_nascimento, tipo)
    VALUES (?, ?, ?, ?, 'moderador')
    ''', (nome, email, senha, data_nascimento))

    # Confirmar as alterações
    conn.commit()
    
    # Fechar a conexão
    conn.close()

# Executar a função para criar as tabelas
if __name__ == '__main__':
    criar_tabelas()
    print("Tabelas criadas com sucesso.")

    # Inserir uma conta de moderador
    inserir_moderador('ADM_SUPREMO', 'moderadorgatinho@gmail.com', 'coxinha123', '2000-01-01')
    print("Conta de moderador inserida com sucesso.")
