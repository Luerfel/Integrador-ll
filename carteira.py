from flask import Flask, request, redirect, url_for, render_template , flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'data/database.db')

@app.route('/static/<path:path>')
def serve_static(path):
    """
Função para servir arquivos estáticos.

Esta função serve arquivos estáticos, como CSS, JavaScript, e imagens,
a partir do diretório /static, com base no caminho especificado.

Uso: Esta função é chamada automaticamente pelo Flask quando uma rota 
que começa com '/static/' é acessada para carregar um recurso estático.
"""
    with open(f'static/{path}', 'rb') as file:
        return file.read()
    
"POST envia dados no corpo da requisição HTTP"
"método GET, que envia os dados na URL"

@app.route('/gerenciar_carteira', methods=['GET', 'POST'])
def carteira():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    valor = 0  # Valor padrão
    taxa_str = ""
    saldo = 0  # Saldo padrão

    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        action = request.form['action']

        cursor.execute('SELECT saldo FROM CARTEIRAS WHERE id_usuario = ?', (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            valor = resultado[0]
        else:
            valor = 0  # Caso o usuário não seja encontrado

        # Calculando a taxa com base no saldo
        if valor <= 100:
            taxa = 0.04 * valor
            taxa_str = "4%"
        elif valor > 100 and valor <= 1000:
            taxa = 0.03 * valor
            taxa_str = "3%"
        elif valor > 1001 and valor <= 5000:
            taxa = 0.02 * valor
            taxa_str = "2%"
        elif valor > 5000 and valor < 100000:
            taxa = 0.01 * valor
            taxa_str = "1%"
        else:
            taxa = 0
            taxa_str = "Isenção de taxa"

        # Lógica de saque
        if 'sacar' in request.form:
            # Calculando o valor a ser sacado e o novo saldo
            valor_saque = valor - taxa
            saldo = valor - valor_saque
        
        # Lógica de adicionar créditos
        elif 'btn-adicionar' in request.form:
            quantidade = float(request.form['quantidade'])
            saldo = valor + quantidade

        cursor.execute('UPDATE CARTEIRAS SET saldo = ? WHERE id_usuario = ?', (saldo, id_usuario))
        conn.commit()
        
        conn.close()
        
        return render_template('gerenciar_carteira.html', valor=valor, taxa_str=taxa_str, saldo=saldo)

    conn.close()

    return render_template('gerenciar_carteira.html', valor=valor, taxa_str=taxa_str, saldo=saldo)



if __name__ == '__main__':
    app.run(debug=True)
