from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

app = Flask(__name__)
database_path = os.path.join(os.getcwd(), 'data/database.db')  # Defina o caminho para o banco de dados

@app.route('/gerenciar_carteira', methods=['GET', 'POST'])
def carteira_ver_saldo():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    valor = 0  # Valor padrão
    taxa_str = ""
    
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        
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
        
        return render_template('gerenciar_carteira.html', valor=valor, taxa_str=taxa_str)
    
    conn.close()
    return render_template('gerenciar_carteira.html', valor=valor, taxa_str=taxa_str)


@app.route('/sacar', methods=['POST'])
def carteira_sacar():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    id_usuario = request.form['id_usuario']
    
    # Buscar o saldo atual do usuário
    cursor.execute('SELECT saldo FROM CARTEIRAS WHERE id_usuario = ?', (id_usuario,))
    resultado = cursor.fetchone()

    if resultado:
        saldo = resultado[0]
        taxa = 0

        # Calculando a taxa com base no saldo
        if saldo <= 100:
            taxa = 0.04 * saldo
        elif saldo > 100 and saldo <= 1000:
            taxa = 0.03 * saldo
        elif saldo > 1001 and saldo <= 5000:
            taxa = 0.02 * saldo
        elif saldo > 5000 and saldo < 100000:
            taxa = 0.01 * saldo

        # Verificar se é saque ou adição de saldo
        if 'btn-sacar' in request.form:
            valor_saque = float(request.form['valor_saque'])
            saldo -= (valor_saque + taxa)  # Subtrai o valor sacado e a taxa
        elif 'btn-adicionar' in request.form:
            valor_adicionar = float(request.form['valor_adicionar'])
            saldo += valor_adicionar

        # Atualizar o saldo do usuário no banco de dados
        cursor.execute('UPDATE CARTEIRAS SET saldo = ? WHERE id_usuario = ?', (saldo, id_usuario))
        conn.commit()

    conn.close()

    return render_template('gerenciar_carteira.html', saldo=saldo)


if __name__ == '__main__':
    app.run(debug=True)
