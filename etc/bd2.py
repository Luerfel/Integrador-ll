import sqlite3

def conectar_db():
    # Atualize o caminho do banco de dados se necessário
    return sqlite3.connect('data/database.db')



def insert_events(conn):
    # Obtém um id_criador válido da tabela 'usuarios'
    cursor = conn.execute('SELECT id FROM usuarios')
    users = cursor.fetchall()
    if not users:
        print("Nenhum usuário encontrado na tabela 'usuarios'. Não é possível inserir eventos.")
        return
    id_criador = users[0][0]  # Usa o id do primeiro usuário
    # Prepara os dados dos eventos
    events = [
        ('Evento 1', 'Descrição 1', 10.0, '2024-10-29', '2024-10-20', '2024-10-28', 'pendente', id_criador),
        ('Evento 2', 'Descrição 2', 15.0, '2024-10-30', '2024-10-21', '2024-10-29', 'pendente', id_criador),
        ('Evento 3', 'Descrição 3', 20.0, '2024-10-30', '2024-10-22', '2024-10-29', 'pendente', id_criador),
    ]
    conn.executemany('''
        INSERT INTO eventos (
            titulo, descricao, valor_cota, data_evento, data_inicio_apostas,
            data_fim_apostas, status, id_criador
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', events)
    conn.commit()
    print("3 eventos inseridos com sucesso.")

def delete_all_events(conn):
    conn.execute('DELETE FROM eventos')
    conn.commit()
    print("Todos os eventos foram deletados da tabela 'eventos'.")

def main():
    conn = conectar_db()
    conn.execute('PRAGMA foreign_keys = ON')  # Habilita as restrições de chave estrangeira

    while True:
        print("\nMenu:")
        print("1 - Inserir 3 eventos")
        print("2 - Deletar todos os eventos da tabela")
        print("0 - Sair")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            insert_events(conn)
        elif choice == '2':
            delete_all_events(conn)
        elif choice == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")
    conn.close()

if __name__ == '__main__':
    main()
