import sqlite3
from datetime import datetime, timedelta
import random

# Conectar ao banco de dados
database_path = 'Integrador-ll/data/database.db'  # Atualize o caminho se necessário
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Função para gerar um título de evento
def gerar_titulo(index):
    return f"Evento Teste {index}"

# Função para gerar uma descrição de evento
def gerar_descricao(index):
    return f"Descrição para o Evento Teste {index}. Este é um evento gerado automaticamente para testes."

# Função para gerar um valor de cota
def gerar_valor_cota():
    return round(random.uniform(1.00, 10.00), 2)

# Função para gerar uma data de evento
def gerar_data_evento(index):
    return (datetime.now() + timedelta(days=index)).strftime('%Y-%m-%d')

# Função para gerar um período de apostas
def gerar_periodo_apostas():
    return "2024-08-20 a 2024-08-25"

# Função para gerar um id_criador (assumindo que já há usuários no banco de dados)
def obter_id_criador():
    cursor.execute('SELECT id FROM usuarios ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    return result[0] if result else 1

# Inserir 20 eventos na tabela
for i in range(1, 21):
    titulo = gerar_titulo(i)
    descricao = gerar_descricao(i)
    valor_cota = gerar_valor_cota()
    data_evento = gerar_data_evento(i)
    periodo_apostas = gerar_periodo_apostas()
    id_criador = obter_id_criador()

    cursor.execute('''
        INSERT INTO eventos (titulo, descricao, valor_cota, data_evento, periodo_apostas, id_criador)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titulo, descricao, valor_cota, data_evento, periodo_apostas, id_criador))

# Salvar as mudanças e fechar a conexão
conn.commit()
conn.close()

print("20 eventos foram gerados e inseridos na tabela 'eventos'.")
