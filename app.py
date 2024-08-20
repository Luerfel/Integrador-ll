from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

app = Flask(__name__)

# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'data/database.db')

# Função para verificar as credenciais
def check_credentials(email, senha):
    # Conecta ao banco de dados
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Consulta para verificar se o email e a senha correspondem a um usuário existente
    cursor.execute('SELECT tipo FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    result = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conn.close()

    # Se a consulta retornar um resultado, as credenciais são válidas
    if result:
        return result[0]  # Retorna o tipo de usuário ('usuario' ou 'moderador')
    return None  # Retorna None se as credenciais forem inválidas

# Rota principal (login)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Coleta os dados do formulário de login
        email = request.form['email']
        senha = request.form['senha']
        tipo_usuario = check_credentials(email, senha)

        # Verifica o tipo de usuário e redireciona para a área correspondente
        if tipo_usuario == 'usuario':
            return '/area_usuario'  # Retorna a URL para a área do usuário
        elif tipo_usuario == 'moderador':
            return '/area_moderador'  # Retorna a URL para a área do moderador
        else:
            return 'Credenciais inválidas', 401  # Retorna uma mensagem de erro e o status 401 (não autorizado)

    # Se o método for GET, renderiza a página de login
    return render_template('index.html')

# Rota para a área do usuário
@app.route('/area_usuario')
def area_usuario():
    return render_template('area_usuario.html')  # Renderiza a página da área do usuário

# Rota para a área do moderador
@app.route('/area_moderador')
def area_moderador():
    return render_template('area_moderador.html')  # Renderiza a página da área do moderador

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')  # Renderiza a página de cadastro

# Servir arquivos estáticos (CSS, JS, imagens)
@app.route('/static/<path:path>')
def serve_static(path):
    # Serve arquivos estáticos a partir do diretório /static
    with open(f'static/{path}', 'rb') as file:
        return file.read()

if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo Flask no modo debug
