from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

app = Flask(__name__)

# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'data/database.db')

# Função para verificar as credenciais
def check_credentials(email, senha):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Consulta para verificar o email e a senha
    cursor.execute('SELECT tipo FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    result = cursor.fetchone()

    conn.close()

    # Retorna o tipo de usuário se as credenciais estiverem corretas
    if result:
        return result[0]
    return None

# Rota para a página inicial (login)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        tipo_usuario = check_credentials(email, senha)

        if tipo_usuario == 'usuario':
            return redirect(url_for('area_usuario'))
        elif tipo_usuario == 'moderador':
            return redirect(url_for('area_moderador'))
        else:
            return 'Credenciais inválidas', 401
    return render_template('index.html')

# Rota para a área do usuário
@app.route('/area_usuario')
def area_usuario():
    return render_template('area_usuario.html')

# Rota para a área do moderador
@app.route('/area_moderador')
def area_moderador():
    return render_template('area_moderador.html')

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Servir arquivos estáticos (CSS, JS, imagens)
@app.route('/static/<path:path>')
def serve_static(path):
    with open(f'static/{path}', 'rb') as file:
        return file.read()

if __name__ == '__main__':
    app.run(debug=True)
