from flask import Flask, request, redirect, url_for, render_template , flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'data/database.db')

@app.route('/gerenciar_carteira', methods=['GET', 'POST'])
def carteira():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    valor = 0
    taxa_str = ''
    saldo = 0

    if request.method == 'POST':
        botao_pressionado = request.form.get('botao')

        if botao_pressionado == 'ver_saldo':
            id_usuario = request.form['id_usuario']

            # Verifica o saldo do usuário
            cursor.execute('SELECT saldo FROM CARTEIRAS WHERE id_usuario = ?', (id_usuario,))
            resultado = cursor.fetchone()

            if resultado:
                valor = resultado[0]
            else:
                valor = 0

            print(f"Saldo inicial: {valor}")

            # Calcula a taxa
            if valor <= 100:
                taxa = 0.04 * valor
                taxa_str = "4%"
            elif valor <= 1000:
                taxa = 0.03 * valor
                taxa_str = "3%"
            elif valor <= 5000:
                taxa = 0.02 * valor
                taxa_str = "2%"
            elif valor < 100000:
                taxa = 0.01 * valor
                taxa_str = "1%"
            else:
                taxa = 0
                taxa_str = "Isenção de taxa"

        if botao_pressionado == 'sacar':
            if valor >= taxa:
                saldo = valor - taxa
            else:
                saldo = valor


        if botao_pressionado == 'btn-adicionar':
            quantidade = float(request.form['quantidade'])
            saldo = valor + quantidade

        # Atualiza o saldo no banco de dados
        cursor.execute('UPDATE CARTEIRAS SET saldo = ? WHERE id_usuario = ?', (saldo, id_usuario))
        conn.commit()
        conn.close()

        return render_template('gerenciar_carteira.html', valor=valor, taxa_str=taxa_str, saldo=saldo)

    conn.close()
    return render_template('gerenciar_carteira.html', valor=valor, taxa_str=taxa_str, saldo=saldo)


if __name__ == '__main__':    
    app.run(debug=True)