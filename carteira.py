from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

app = Flask(__name__)
database_path = os.path.join(os.getcwd(), 'data/database.db')

@app.route('/ver_saldo', methods=['GET', 'POST'])
def carteira_ver_saldo():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    valor = 0  # Valor padrão
    
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        
        cursor.execute('SELECT saldo FROM CARTEIRAS WHERE id_usuario = ?', (id_usuario,))
        resultado = cursor.fetchone()

        if resultado:
            valor = resultado[0]
        else:
            valor = 0  # Caso o usuário não seja encontrado

        
        return render_template('gerenciar_carteira.html', valor=valor)
    
    conn.close()
    return render_template('gerenciar_carteira.html', valor=valor)


@app.route('/sacar', methods=['POST', 'GET'])
def carteira_sacar():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if request.method == 'POST':        
        id_usuario = request.form['id_usuario1']
                
        # Buscar o saldo atual do usuário
        cursor.execute('SELECT saldo FROM CARTEIRAS WHERE id_usuario = ?', (id_usuario,))
        result = cursor.fetchone()

        if result is not None:
            saldo = result[0]  # Extrai o valor do saldo da tupla
        else:
            saldo = 0  # Ou um valor padrão, se preferir

            # Verificar se é saque ou adição de saldo
        valor_saque = float(request.form['valor_saque'])
        if 'btn-sacar' in request.form:
            id_usuario = request.form['id_usuario1']

            # Calculando a taxa com base no valor a ser sacado
            if valor_saque <= 100:
                taxa = 0.04 * valor_saque
                taxa_str = "4%"
            elif valor_saque > 100 and valor_saque <= 1000:
                taxa = 0.03 * valor_saque
                taxa_str = "3%"
            elif valor_saque > 1001 and valor_saque <= 5000:
                taxa = 0.02 * valor_saque
                taxa_str = "2%"
            elif valor_saque > 5000 and valor_saque < 100000:
                taxa = 0.01 * valor_saque
                taxa_str = "1%"
            saldo = saldo - (valor_saque + taxa)  # Subtrai o valor sacado e a taxa
        # Atualizar o saldo do usuário no banco de dados
        cursor.execute('UPDATE CARTEIRAS SET saldo = ? WHERE id_usuario = ?', (saldo, id_usuario))
        conn.commit()
        return render_template('gerenciar_carteira.html', saldo=saldo, taxa=taxa, taxa_str=taxa_str)


@app.route('/adicionar', methods=['POST', 'GET'])

def carteira_adicionar():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if request.method == 'POST':        
        id_usuario = request.form['id_usuario2']
                    
        # Buscar o saldo atual do usuário
        cursor.execute('SELECT saldo FROM CARTEIRAS WHERE id_usuario = ?', (id_usuario,))
        result = cursor.fetchone()

        if result is not None:
            saldo = result[0]  # Extrai o valor do saldo da tupla
        else:
            saldo = 0  # Ou um valor padrão, se preferir

        if 'btn-adicionar' in request.form:
            id_usuario = request.form['id_usuario2']
            valor_adicionar = float(request.form['valor_adicionar'])
            saldo = saldo + valor_adicionar

        # Atualizar o saldo do usuário no banco de dados
        cursor.execute('UPDATE CARTEIRAS SET saldo = ? WHERE id_usuario = ?', (saldo, id_usuario))
        conn.commit()
        return render_template('gerenciar_carteira.html', saldo=saldo)

    conn.close()

    return render_template('gerenciar_carteira.html', saldo=saldo)


if __name__ == '__main__':
    app.run(debug=True)
