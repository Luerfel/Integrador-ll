import sqlite3
import os
import platform
from tabulate import tabulate #pip install tabulate

def conectar_db():
    # Atualize o caminho do banco de dados se necessário
    return sqlite3.connect('data/database.db')

def limpar_terminal():
    # Detecta o sistema operacional  
    sistema_operacional = platform.system()

    if sistema_operacional == "Windows":
        # Comando para limpar o terminal no Windows
        os.system('cls')
    else:
        # Comando para limpar o terminal em Linux e MacOS
        os.system('clear')

def criar_tabelas():
    # Conectar ao banco de dados (ou criar, se não existir)
    conn = conectar_db()
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
        data_inicio_apostas DATE NOT NULL,
        data_fim_apostas DATE NOT NULL,
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
    conn.close()

def inserir_moderador(nome, email, senha, data_nascimento):
    # Conectar ao banco de dados
    conn = conectar_db()
    cursor = conn.cursor()

    # Inserir novo moderador na tabela usuarios
    cursor.execute('''
    INSERT INTO usuarios (nome, email, senha, data_nascimento, tipo)
    VALUES (?, ?, ?, ?, 'moderador')
    ''', (nome, email, senha, data_nascimento))

    # Confirmar as alterações
    conn.commit()
    conn.close()
    
def exibir_tabela(nome_tabela):
    conn = conectar_db()
    cursor = conn.cursor()
    limpar_terminal()

    try:
        cursor.execute(f'SELECT * FROM {nome_tabela}')
        rows = cursor.fetchall()

        if rows:
            # Obter os nomes das colunas
            colunas = [description[0] for description in cursor.description]
            
            # Exibir os dados em uma tabela formatada
            print(f'\nConteúdo da tabela {nome_tabela}:')
            print(tabulate(rows, headers=colunas, tablefmt="grid"))
        else:
            print(f"\nA tabela {nome_tabela} está vazia.")
    except sqlite3.Error as e:
        print(f"Erro ao consultar a tabela {nome_tabela}: {e}")
    finally:
        conn.close()

    input("Pressione Enter para continuar")
def menu():
    while True:
        limpar_terminal()
        print("\nMenu:")
        print("1. Criar Tabelas")
        print("2. Inserir Moderador")
        print("3. Consultar Usuários")
        print("4. Consultar Eventos")
        print("5. Consultar Categorias de Eventos")
        print("6. Consultar Eventos Categorias")
        print("7. Consultar Carteiras")
        print("8. Consultar Transações")
        print("9. Consultar Apostas")
        print("10. Consultar Resultados de Eventos")
        print("11. Consultar Moderações de Eventos")
        print("0. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            criar_tabelas()
            print("Tabelas criadas com sucesso.")
        elif escolha == '2':
            nome = input("Nome do moderador: ")
            email = input("Email do moderador: ")
            senha = input("Senha do moderador: ")
            data_nascimento = input("Data de nascimento (YYYY-MM-DD): ")
            inserir_moderador(nome, email, senha, data_nascimento)
            print("Conta de moderador inserida com sucesso.")
        elif escolha == '3':
            exibir_tabela('usuarios')
        elif escolha == '4':
            exibir_tabela('eventos')
        elif escolha == '5':
            exibir_tabela('categorias_eventos')
        elif escolha == '6':
            exibir_tabela('eventos_categorias')
        elif escolha == '7':
            exibir_tabela('carteiras')
        elif escolha == '8':
            exibir_tabela('transacoes')
        elif escolha == '9':
            exibir_tabela('apostas')
        elif escolha == '10':
            exibir_tabela('resultados_eventos')
        elif escolha == '11':
            exibir_tabela('moderacoes_eventos')
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def verificar_saldo(id_usuario):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT saldo FROM carteiras WHERE id_usuario = ?", (id_usuario,))
    saldo = cursor.fetchone()

    conn.close()
    return saldo[0] if saldo else None

def atualizar_saldo(id_usuario, valor):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE carteiras SET saldo = saldo + ? WHERE id_usuario = ?", (valor, id_usuario))
    conn.commit()
    conn.close()

def registrar_aposta(id_usuario, id_evento, valor, opcao):
    saldo = verificar_saldo(id_usuario)
    if saldo is None:
        print("Usuário não possui carteira.")
        return

    if saldo < valor:
        print("Saldo insuficiente para realizar a aposta.")
        return

    # Deduzir o valor da aposta e registrar a transação
    atualizar_saldo(id_usuario, -valor)

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO apostas (id_evento, id_usuario, valor, opcao)
    VALUES (?, ?, ?, ?)
    ''', (id_evento, id_usuario, valor, opcao))

    conn.commit()
    conn.close()
    print("Aposta registrada com sucesso.")

if __name__ == '__main__':
    menu()
