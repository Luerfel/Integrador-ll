from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os


app = Flask(__name__)

# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'data/database.db')

def criar_aposta():
    while True:
        opcao = input("Deseja criar um evento? (S/N): ")
        if opcao.lower() == 's':
            titulo = input("Título do evento (até 50 caracteres): ")
            descricao = input("Descrição (até 150 caracteres): ")
            valor_cota = float(input("Valor da cota (R$1,00 mínimo) R$: "))
            data_evento = input("Data do evento (dia/mês/ano): ")
            periodo_apostas = input("""Digite o perído de apostas 
            conforme o padrão:\n
            Início dia/mês/ano - hora/minuto/segundo\n
            Fim dia/mês/ano - hora/minuto/segundo: """)
            id_criador = int(input("ID do criador do evento: "))

            # Validações
            if len(titulo) > 50:
                print("O título deve ter no máximo 50 caracteres.")
                continue
            if len(descricao) > 150:
                print("A descrição deve ter no máximo 150 caracteres.")
                continue
            if valor_cota < 1.00:
                print("O valor da cota deve ser no mínimo R$1,00.")
                continue
            # Inserindo os dados na tabela
            try:
                conn = sqlite3.connect(database_path)
                cursor = conn.cursor()
                sql = '''INSERT INTO eventos (titulo, descricao, valor_cota, data_evento, periodo_apostas, id_criador)
                         VALUES (?, ?, ?, ?, ?, ?)'''
                values = (titulo, descricao, valor_cota, data_evento, periodo_apostas, id_criador)
                cursor.execute(sql, values)
                conn.commit()
                print("Evento criado com sucesso!")
            except sqlite3.Error as e:
                print(f"Erro ao inserir no banco de dados: {e}")
            finally:
                conn.close()
        elif opcao.lower() == 'n':
            break
        else:
            print("Opção inválida. Digite 'S' para sim ou 'N' para não.")

if __name__ == "__main__":
    criar_aposta()