from flask import Flask, request, redirect, url_for, render_template , flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'Integrador-ll/data/database.db')

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
    if request.method == 'POST':    
        id_usuario = request.form['id_usuario']
        quantidade = request.form['quantidade']
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    sql = '''SELECT saldo FROM CARTEIRAS WHERE id_usuario = ?'''
    cursor.execute(sql, id_usuario)
    valor = cursor.fetchone()[0]

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
    elif valor > 100000:
        taxa = 0
        taxa_str = "Isenção de taxa"
    
    valor_saque = valor - taxa
    saldo = valor - valor_saque
    sql = '''UPDATE CARTEIRAS SET saldo = ? WHERE id_usuario = ?'''
    cursor.execute(sql, saldo, id_usuario )
    
    return render_template('gerenciar_carteira.html', valor=valor, taxa_str = taxa_str, saldo=saldo, quantidade = quantidade)





if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo Flask no modo debug
