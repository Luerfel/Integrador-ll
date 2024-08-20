from flask import Flask
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
@app.route('/')
def home():
    with open('templates/index.html', 'r') as file:
        return file.read()

# Rota para tratar o login
@app.route('/login/<email>/<senha>')
def login(email, senha):
    tipo_usuario = check_credentials(email, senha)

    if tipo_usuario == 'usuario':
        with open('templates/area_usuario.html', 'r') as file:
            return file.read()
    elif tipo_usuario == 'moderador':
        with open('templates/area_moderador.html', 'r') as file:
            return file.read()
    else:
        return 'Credenciais inválidas'

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    with open('templates/cadastro.html', 'r') as file:
        return file.read()

# Servir arquivos estáticos (CSS, JS, imagens)
@app.route('/static/<path:path>')
def serve_static(path):
    with open(f'static/{path}', 'rb') as file:
        return file.read()

if __name__ == '__main__':
    app.run(debug=True)
