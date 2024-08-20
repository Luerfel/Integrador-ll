from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os
import re

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
    
"--------------------------------------------------------------------------------------------------------------------------------------------------------------"

"LOGIN"

# Função para verificar as credenciais
def check_credentials(email, senha):
    """
Esta função verifica as credenciais do usuário consultando o banco de dados SQLite.
Recebe o email e a senha como parâmetros.
Executa uma consulta no banco de dados para verificar se há uma correspondência.
Retorna o tipo de usuário ('usuario' ou 'moderador') se as credenciais forem válidas, ou None se
não forem.

Uso: Esta função é usada para validar as credenciais do usuário durante o processo de login
"""

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
    """
Esta função trata tanto requisições GET quanto POST na rota raiz ('/').
- Se for uma requisição GET, ela simplesmente renderiza a página de login (index.html).
- Se for uma requisição POST, ela coleta o email e a senha fornecidos, verifica as credenciais no
banco de dados usando a função check_credentials(), e redireciona o usuário para a página
correspondente ao seu tipo (usuário ou moderador).
- Se as credenciais forem inválidas, retorna uma mensagem de erro e o código HTTP 401.

Uso: Esta função é chamada quando o usuário tenta acessar a página de login ou submete o
formulário de login.
  """
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
    """
Esta função simplesmente renderiza a página HTML correspondente à área do usuário comum
(area_usuario.html).

Uso: Esta função é chamada quando um usuário comum faz login com sucesso
"""
    return render_template('area_usuario.html')  # Renderiza a página da área do usuário

# Rota para a área do moderador
@app.route('/area_moderador')

def area_moderador():
    """
Esta função renderiza a página HTML correspondente à área do moderador
(area_moderador.html).

Uso: Esta função é chamada quando um moderador faz login com sucesso.
"""
    return render_template('area_moderador.html')  # Renderiza a página da área do moderador

"--------------------------------------------------------------------------------------------------------------------------------------------------------------"







"CADASTRO"



def is_valid_email(email):
    """
Esta função verifica se um email contém os caracteres "@" e "." 
nas posições corretas para ser considerado válido.

Uso: Esta função é chamada durante o processo de cadastro para garantir que o email fornecido esteja em um formato minimamente aceitável.
"""
    if "@" in email and "." in email:
        at_index = email.index("@")
        dot_index = email.rindex(".")
        # Verifica se o "@" não está no início ou no final, 
        # e se o "." está depois do "@" e não no final.
        if at_index > 0 and dot_index > at_index + 1 and dot_index < len(email) - 1:
            return True
    return False

@app.route('/cadastro', methods=['GET', 'POST'])

def cadastro():
    """
Função para gerenciar o cadastro de novos usuários.

Esta função lida com as requisições GET e POST na rota '/cadastro'.
- Se o método for POST, valida o email, tenta inserir o usuário no banco de dados,
  e retorna uma mensagem de erro se o email já estiver cadastrado ou se ocorrer um erro inesperado.
- Se o método for GET, renderiza a página de cadastro.

Uso: Esta função é chamada quando um usuário tenta se cadastrar na aplicação.
"""
    error_message = None  # Variável para armazenar a mensagem de erro

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        data_nascimento = request.form['data_nascimento']

        # Validação do email 
        if not is_valid_email(email):
            error_message = 'Email inválido.'

        else:
            # Conectar ao banco de dados e inserir o novo usuário
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()

            try:
                cursor.execute('''
                    INSERT INTO usuarios (nome, email, senha, data_nascimento)
                    VALUES (?, ?, ?, ?)
                ''', (nome, email, senha, data_nascimento))

                conn.commit()
                return redirect(url_for('home'))

            except sqlite3.IntegrityError:
                error_message = 'Erro: Email já cadastrado. Tente novamente com um email diferente.'

            except Exception as e:
                # Tratamento genérico de erros
                error_message = f'Erro inesperado: {e}'

            finally:
                conn.close()

    return render_template('cadastro.html', error_message=error_message)

"--------------------------------------------------------------------------------------------------------------------------------------------------------------"


if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo Flask no modo debug
