from flask import Flask, request, redirect, url_for, render_template
import sqlite3
import os

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
            return '/moderador_dashboard'  # Retorna a URL para a área do moderador
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

"moderador"

@app.route('/moderador_dashboard', methods=['GET'])
def moderador_dashboard():
    """
    Função para gerenciar a exibição do dashboard do moderador.

    Esta função lida com as requisições GET na rota '/moderador_dashboard'.
    - Obtém o parâmetro de consulta 'view' da URL, que define qual visualização o moderador quer acessar (pendentes ou finalizados).
    - Com base no parâmetro 'view', define um filtro de status para a consulta SQL, que pode ser 'pendente' ou 'aprovado'.
    - Conecta ao banco de dados SQLite e executa uma consulta para selecionar todos os eventos que correspondem ao status filtrado.
    - Renderiza o template 'area_moderador.html', passando os eventos e a view atual para serem exibidos na interface.

    Uso: Esta função é chamada quando um moderador acessa o dashboard para ver eventos pendentes de aprovação ou eventos que já foram aprovados.
    """
    # Obtém o parâmetro de consulta 'view' da URL, com o valor padrão 'pendentes'
    view = request.args.get('view', 'pendentes')
    # Define o filtro de status com base no valor de 'view'
    status_filter = 'pendente' if view == 'pendentes' else 'aprovado'

    # Conecta ao banco de dados SQLite
    with sqlite3.connect(database_path) as conn:
        conn.row_factory = sqlite3.Row  # Configura a fábrica de linhas para acessar colunas por nome
        # Executa a consulta para selecionar eventos com o status especificado
        eventos = conn.execute('SELECT * FROM eventos WHERE status = ?', (status_filter,)).fetchall()

    # Renderiza o template 'area_moderador.html', passando os eventos e a view atual
    return render_template('area_moderador.html', eventos=eventos, view=view)


@app.route('/acao_evento', methods=['POST'])
def acao_evento():
    """
    Função para processar as ações realizadas pelos moderadores sobre os eventos.

    Esta função lida com as requisições POST na rota '/acao_evento'.
    - Recebe o ID do evento, a ação a ser realizada (aprovar, reprovar, confirmar, não ocorrido) e, opcionalmente, o motivo de reprovação.
    - Mapeia a ação recebida para os status e dados extras correspondentes, a serem armazenados no banco de dados.
    - Conecta ao banco de dados SQLite e realiza as operações de atualização ou inserção necessárias:
      - Atualiza o status do evento de acordo com a ação escolhida.
      - Se a ação for 'reprovar', insere um registro na tabela 'moderacoes_eventos' com o motivo de reprovação.
      - Para as ações 'reprovar', 'confirmar' ou 'nao_ocorrido', insere um registro na tabela 'resultados_eventos' com o resultado do evento.
    - Retorna uma resposta HTTP adequada (200 para sucesso ou 500 em caso de erro).

    Uso: Esta função é chamada quando um moderador realiza alguma ação em um evento na interface da área do moderador.
    """
    # Obtém os dados do formulário
    evento_id = request.form.get('evento_id')
    acao = request.form.get('acao')
    motivo_rejeicao = request.form.get('motivo_rejeicao', '')
    id_moderador = 1  # ID do moderador fixo ou pode ser passado via request/form.

    # Mapeamento das ações para status e dados adicionais
    acao_map = {
        'aprovar': ('aprovado', None),
        'reprovar': ('reprovado', motivo_rejeicao),
        'confirmar': ('finalizado', 'ocorrido'),
        'nao_ocorrido': ('finalizado', 'não ocorrido')
    }

    # Validações iniciais dos dados recebidos
    if not evento_id or acao not in acao_map:
        return 'Dados inválidos', 400

    try:
        # Conecta ao banco de dados SQLite
        with sqlite3.connect(database_path) as conn:
            status, extra_data = acao_map[acao]
            # Atualiza o status do evento com base na ação
            conn.execute('UPDATE eventos SET status = ? WHERE id = ?', (status, evento_id))
            
            # Se a ação for 'reprovar', insere um registro na tabela de moderações
            if acao == 'reprovar':
                conn.execute('''
                    INSERT INTO moderacoes_eventos (id_evento, id_moderador, acao, motivo_rejeicao) 
                    VALUES (?, ?, ?, ?)
                ''', (evento_id, id_moderador, acao, motivo_rejeicao))
            
            # Insere um registro na tabela de resultados se a ação for 'reprovar', 'confirmar' ou 'não_ocorrido'
            if acao in ['reprovar', 'confirmar', 'nao_ocorrido']:
                conn.execute('''
                    INSERT INTO resultados_eventos (id_evento, resultado) 
                    VALUES (?, ?)
                ''', (evento_id, extra_data))
            
            # Confirma as operações no banco de dados
            conn.commit()
            return '', 200
    except Exception as e:
        # Em caso de erro, retorna o erro e um status 500
        print(f"Erro ao processar ação: {e}")
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo Flask no modo debug
