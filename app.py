from flask import Flask, request, redirect, url_for, render_template, flash, get_flashed_messages, session, jsonify
import sqlite3
import os
from datetime import datetime,timedelta #pip install datetime
import smtplib; #pip install secure-smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


app = Flask(__name__)
# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'data/database.db')
app.secret_key = 'macaco'



def get_user_id():
 # usamos para obter o id do usuario e usar na seassion
    email = session.get('email')
    if email:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
    return None

def obter_id_usuario():
    return session.get('id_usuario')


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

    cursor.execute('SELECT id, tipo FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    result = cursor.fetchone()
    conn.close()
    if result:
        session['id_usuario'] = result[0]  # Armazena o id do usuário na sessão
        return result[1]  # Retorna o tipo de usuário
    else:
        return None

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
        email = request.form['email']
        senha = request.form['senha']
        tipo_usuario = check_credentials(email, senha)

        if tipo_usuario == 'usuario':
            session['logged_in'] = True
            session['user_type'] = 'usuario'
            session['email'] = email
            return '/area_usuario'
        elif tipo_usuario == 'moderador':
            session['logged_in'] = True
            session['user_type'] = 'moderador'
            session['email'] = email
            return '/moderador_dashboard'
        else:
            return 'Credenciais inválidas', 401

    return render_template('index.html')
"AREA DO USUARIOOOOOOOOOOOOOOOOOOOOOOOO"
@app.route('/area_usuario')
def area_usuario():
    """
    Esta função lida com a rota '/area_usuario' e exibe a área do usuário, que inclui eventos
    finalizando hoje, eventos mais apostados e categorias de eventos, caso o usuário esteja logado.

    - Verifica se o usuário está autenticado verificando a chave 'logged_in' na sessão.
    - Se o usuário estiver logado, a função busca eventos finalizando no dia corrente, eventos
      mais apostados e as categorias de eventos no banco de dados.
    - Caso o usuário não esteja autenticado, ele é redirecionado para a página de login.

    Funcionalidades:
    1. Obter os eventos cujas apostas estão finalizando hoje e que possuem status 'aprovado'.
       - A consulta é limitada a 10 eventos ordenados pela data do evento.
    2. Obter os eventos mais apostados, calculando o valor total apostado em cada evento.
       - A consulta retorna os 10 eventos com maior soma de apostas e os ordena de forma
         decrescente.
    3. Obter todas as categorias de eventos.

    Após obter os dados, a função renderiza a página 'area_usuario.html', passando como contexto
    os eventos finalizando hoje, os eventos mais apostados e as categorias.

    Uso: Esta função é chamada quando o usuário autenticado acessa a área de usuário após fazer login.
    Se o usuário não estiver logado, ele será redirecionado para a página de login.

    Retorno:
    - Se o usuário estiver logado: Renderiza a página 'area_usuario.html' com os dados dos eventos e
      categorias.
    - Se o usuário não estiver logado: Redireciona para a rota de login ('/login').
    """
    if 'logged_in' in session:
        user_id = session.get('id_usuario')
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        print("ID do usuário na sessão:", session.get('id_usuario'))

        # Obter eventos com período de apostas finalizando hoje
        cursor.execute('''
            SELECT * FROM eventos
            WHERE DATE(data_fim_apostas) = DATE('now', 'localtime')
            AND status = 'aprovado'
            ORDER BY data_evento ASC
            LIMIT 10
        ''')
        eventos_finalizando = cursor.fetchall()

        # Obter eventos mais apostados
        cursor.execute('''
            SELECT eventos.*, SUM(apostas.valor) as total_apostado
            FROM eventos
            LEFT JOIN apostas ON eventos.id = apostas.id_evento
            WHERE eventos.status = 'aprovado'
            AND data_evento > date('now')
            GROUP BY eventos.id
            ORDER BY total_apostado DESC
            LIMIT 10
        ''')
        eventos_mais_apostados = cursor.fetchall()

        # Obter eventos disponíveis
        cursor.execute('''
            SELECT eventos.*, SUM(apostas.valor) as total_apostado
            FROM eventos
            LEFT JOIN apostas ON eventos.id = apostas.id_evento
            WHERE eventos.status = 'aprovado'
            GROUP BY eventos.id
            ORDER BY data_fim_apostas DESC
        ''')
        eventos = cursor.fetchall()

        # Obter categorias
        cursor.execute('SELECT * FROM categorias_eventos')
        categorias = cursor.fetchall()

        conn.close()

        return render_template('area_usuario.html', eventos_finalizando=eventos_finalizando,
                               eventos_mais_apostados=eventos_mais_apostados, categorias=categorias,
                               eventos=eventos)
    else:
        return redirect(url_for('login'))
    


"------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
"PESQUISAR EVENTO"
@app.route('/pesquisar_evento', methods=['GET'])
def pesquisar_evento():
    """
    Esta função trata requisições GET na rota '/pesquisar_evento' e permite aos usuários pesquisar
    eventos com base em uma consulta de texto (query), categoria, data e ordenação. A função também
    suporta paginação para facilitar a navegação pelos resultados.

    Funcionalidades:
    1. Coleta os parâmetros da URL (query, categoria, data, ordenação e página) para aplicar os filtros
       e configurar a paginação.
    2. Realiza uma consulta SQL no banco de dados para buscar eventos que correspondam aos critérios
       definidos:
       - Se houver uma 'query', busca no título ou descrição do evento.
       - Se houver uma categoria, filtra os eventos por categoria.
       - Se houver uma data, filtra os eventos por data específica.
       - Aplica a ordenação especificada (popularidade, valor de cota ou data do evento).
    3. Implementa paginação para limitar os resultados a 10 eventos por página.
    4. Busca as categorias de eventos disponíveis para serem exibidas como filtros na interface.

    Uso: Esta função é chamada quando o usuário acessa a página de pesquisa de eventos e pode aplicar
    filtros ou realizar buscas. A resposta renderiza a página 'pesquisar_evento.html' com os eventos
    filtrados e os dados adicionais necessários para a interface de pesquisa.

    Parâmetros de URL aceitos:
    - query: String para busca no título ou descrição do evento.
    - categoria: ID da categoria para filtrar os eventos.
    - data: Data do evento para filtrar.
    - ordenacao: Critério de ordenação (popularidade, valor_cota, data).
    - page: Número da página para implementar a paginação.

    Retorno:
    - Renderiza a página 'pesquisar_evento.html' com os resultados da pesquisa, os eventos e as categorias.
    """
    query = request.args.get('query', '')
    categoria_id = request.args.get('categoria', '')
    data = request.args.get('data', '')
    ordenacao = request.args.get('ordenacao', '')
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Consulta SQL base
    sql = '''
        SELECT DISTINCT eventos.*
        FROM eventos
        LEFT JOIN eventos_categorias ON eventos.id = eventos_categorias.id_evento
        WHERE eventos.status = 'aprovado'
        AND eventos.data_evento >= date('now')

    '''
    params = []

    # Aplicar filtro de busca se houver
    if query:
        sql += ' AND (eventos.titulo LIKE ? OR eventos.descricao LIKE ?)'
        params.extend(['%' + query + '%', '%' + query + '%'])

    # Aplicar filtro de categoria se houver
    if categoria_id:
        sql += ' AND eventos_categorias.id_categoria = ?'
        params.append(categoria_id)

    # Aplicar filtro de data se houver
    if data:
        sql += ' AND eventos.data_evento = ?'
        params.append(data)

    # Aplicar ordenação
    if ordenacao:
        if ordenacao == 'popularidade':
            sql += ' ORDER BY (SELECT COUNT(*) FROM apostas WHERE apostas.id_evento = eventos.id) DESC'
        elif ordenacao == 'valor_cota':
            sql += ' ORDER BY eventos.valor_cota DESC'
        else:
            sql += ' ORDER BY eventos.data_evento ASC'
    else:
        sql += ' ORDER BY eventos.data_evento ASC'

    # Paginação
    sql += ' LIMIT ? OFFSET ?'
    params.extend([per_page, offset])

    cursor.execute(sql, params)
    eventos = cursor.fetchall()

    # Obter categorias para os filtros
    cursor.execute('SELECT * FROM categorias_eventos')
    categorias = cursor.fetchall()

    conn.close()

    return render_template('pesquisar_evento.html', eventos=eventos, query=query, categorias=categorias,
                           categoria_id=categoria_id, data=data, ordenacao=ordenacao, page=page, per_page=per_page)


@app.route('/eventos_categoria/<int:categoria_id>', methods=['GET', 'POST'])
def eventos_por_categoria(categoria_id):
    """
    Esta função trata requisições na rota '/eventos_categoria/<categoria_id>' e exibe os eventos
    de uma categoria específica, determinada pelo ID da categoria fornecido na URL.

    Funcionalidades:
    - Obtém o nome da categoria com base no ID fornecido.
    - Caso a categoria não seja encontrada, retorna um erro 404.
    - Caso a categoria exista, busca os eventos associados a essa categoria no banco de dados e que tenham o status 'aprovado'.
    - Renderiza a página 'eventos_categoria.html', exibindo os eventos da categoria para o usuário.

    Parâmetro de URL:
    - categoria_id: ID da categoria cujos eventos serão exibidos.

    Retorno:
    - Se a categoria for encontrada: Renderiza a página 'eventos_categoria.html' com os eventos da categoria.
    - Se a categoria não for encontrada: Retorna uma mensagem de erro 404.
    """
    conn = sqlite3.connect('data/database.db')  # Atualize o caminho do banco de dados, se necessário
    cursor = conn.cursor()

    # Obter o nome da categoria
    cursor.execute('SELECT nome FROM categorias_eventos WHERE id = ?', (categoria_id,))
    categoria = cursor.fetchone()

    if not categoria:
        conn.close()
        return 'Categoria não encontrada.', 404

    categoria_nome = categoria[0]

    # Obter eventos da categoria com filtro de data
    cursor.execute('''
        SELECT eventos.*
        FROM eventos
        JOIN eventos_categorias ON eventos.id = eventos_categorias.id_evento
        WHERE eventos_categorias.id_categoria = ?
        AND eventos.status = 'aprovado'
        AND eventos.data_evento >= date('now')
        ORDER BY eventos.data_evento ASC
    ''', (categoria_id,))
    eventos = cursor.fetchall()
    conn.close()

    # Caso a requisição seja POST, processar aposta
    if request.method == 'POST':
        if 'logged_in' in session:
            try:
                user_id = session.get('user_id')
                evento_id = request.form['evento_id']
                valor_aposta = float(request.form['valor_aposta'])
                opcao = request.form['aposta']

                # Verificar se o valor da aposta é maior que zero
                if valor_aposta <= 0:
                    flash("Valor da aposta deve ser maior que zero.", 'error')
                    return redirect(url_for('eventos_por_categoria', categoria_id=categoria_id))

                with sqlite3.connect('data/database.db', timeout=5) as conn:
                    cursor = conn.cursor()

                    # Obter o valor da cota do evento
                    cursor.execute('SELECT valor_cota FROM eventos WHERE id = ?', (evento_id,))
                    valor_cota = cursor.fetchone()

                    if valor_cota is not None:
                        valor_cota = valor_cota[0]
                        valor_total_aposta = valor_aposta * valor_cota

                        # Verificar o saldo do usuário
                        cursor.execute('SELECT saldo FROM carteiras WHERE id_usuario = ?', (user_id,))
                        saldo = cursor.fetchone()

                        if saldo is not None and saldo[0] >= valor_total_aposta:
                            # Inserir a aposta
                            cursor.execute('INSERT INTO apostas (id_evento, id_usuario, valor, opcao) VALUES (?, ?, ?, ?)',
                                           (evento_id, user_id, valor_total_aposta, opcao))

                            # Atualizar o saldo do usuário
                            novo_saldo = saldo[0] - valor_total_aposta
                            cursor.execute('UPDATE carteiras SET saldo = ? WHERE id_usuario = ?', (novo_saldo, user_id))

                            # Commit da transação
                            conn.commit()
                            flash("Aposta realizada com sucesso!", 'success')
                        else:
                            flash("Saldo insuficiente para realizar a aposta.", 'error')
                    else:
                        flash("Evento não encontrado.", 'error')

            except sqlite3.Error as e:
                flash(f"Ocorreu um erro ao processar a aposta: {str(e)}", 'error')

        else:
            flash("Por favor, faça login para realizar uma aposta.", 'error')
            return redirect(url_for('login'))

    # Renderizar a página com eventos e nome da categoria
    return render_template('eventos_categoria.html', eventos=eventos, categoria_nome=categoria_nome)


"CADASTRO"

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
    error_message = None

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
                    INSERT INTO usuarios (nome, email, senha, data_nascimento, tipo)
                    VALUES (?, ?, ?, ?, 'usuario')  -- Define o tipo como 'usuario' por padrão
                ''', (nome, email, senha, data_nascimento))
        

                user_id = cursor.lastrowid
                # Criar carteira para o usuário
                cursor.execute('''
                INSERT INTO carteiras (id_usuario, saldo)
                VALUES (?, 0.00)
                ''', (user_id,))
                conn.commit()
                # Autentica o usuário após o cadastro
                session['logged_in'] = True
                session['user_type'] = 'usuario'
                session['email'] = email
                
                # Renderiza a página que pergunta sobre adicionar crédito
                return render_template('ask_add_credit.html')

            except sqlite3.IntegrityError:
                error_message = 'Erro: Email já cadastrado. Tente novamente com um email diferente.'
            except Exception as e:
                error_message = f'Erro inesperado: {e}'
            finally:
                conn.close()

    return render_template('cadastro.html', error_message=error_message)


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

"--------------------------------------------------------------------------------------------------------------------------------------------------------------"

@app.route('/moderador_dashboard', methods=['GET'])
def moderador_dashboard():
    """
    Função para gerenciar a exibição do dashboard do moderador.
    """
    # Obtém o parâmetro de consulta 'view' da URL, com o valor padrão 'pendentes'
    view = request.args.get('view', 'pendentes')

    # Define o filtro de status com base no valor de 'view'
    if view == 'pendentes':
        status_filter = 'pendente'
    elif view == 'finalizar':
        status_filter = 'aprovado'
    else:
        status_filter = 'pendente'

    # Conecta ao banco de dados SQLite
    with sqlite3.connect(database_path) as conn:
        conn.row_factory = sqlite3.Row  # Configura para acessar colunas por nome
        # Seleciona eventos com o status especificado
        eventos = conn.execute('SELECT * FROM eventos WHERE status = ?', (status_filter,)).fetchall()

    # Renderiza o template 'area_moderador.html', passando os eventos e a view atual
    return render_template('area_moderador.html', eventos=eventos, view=view)

@app.route('/acao_evento', methods=['POST'])
def acao_evento():
    """
    Função para processar as ações realizadas pelos moderadores sobre os eventos.
    """
    # Obtém os dados do formulário
    evento_id = request.form.get('evento_id')
    acao = request.form.get('acao')
    motivo_rejeicao = request.form.get('motivo_rejeicao', '')
    id_moderador = 1  # ID do moderador fixo 

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
            conn.row_factory = sqlite3.Row
            status, extra_data = acao_map[acao]
            # Atualiza o status do evento
            conn.execute('UPDATE eventos SET status = ? WHERE id = ?', (status, evento_id))
            
            # Se a ação for 'reprovar', insere um registro na tabela de moderações e envia o e-mail
            if acao == 'reprovar':
                conn.execute('''
                    INSERT INTO moderacoes_eventos (id_evento, id_moderador, acao, motivo_rejeicao) 
                    VALUES (?, ?, ?, ?)
                ''', (evento_id, id_moderador, acao, motivo_rejeicao))

                # Chamar a função para enviar o e-mail de rejeição
                enviar_email_rejeicao(motivo_rejeicao, evento_id)

            # Se a ação for 'reprovar', 'confirmar' ou 'nao_ocorrido', insere um registro nos resultados
            if acao in ['reprovar', 'confirmar', 'nao_ocorrido']:
                conn.execute('''
                    INSERT INTO resultados_eventos (id_evento, resultado) 
                    VALUES (?, ?)
                ''', (evento_id, extra_data))

                # Distribui os prêmios se o evento foi finalizado
                if acao in ['confirmar', 'nao_ocorrido']:
                    distribuir_premios(evento_id, extra_data, conn)
            
            # Confirma as operações no banco de dados
            conn.commit()
            return '', 200
    except Exception as e:
        print(f"Erro ao processar ação: {e}")
        return str(e), 500

def distribuir_premios(evento_id, resultado_evento, conn):
    """
    Função para distribuir prêmios aos usuários que acertaram o resultado do evento.
    """
    try:
        # Obter o valor da cota do evento
        evento = conn.execute('SELECT valor_cota FROM eventos WHERE id = ?', (evento_id,)).fetchone()
        valor_cota = evento['valor_cota']

        # Obter todas as apostas deste evento
        apostas = conn.execute('SELECT * FROM apostas WHERE id_evento = ?', (evento_id,)).fetchall()

        # Mapear as opções das apostas para resultados padronizados
        opcao_para_resultado = {
            'sim': 'ocorrido',
            'nao': 'não ocorrido',
        }

        # Normalizar o resultado do evento
        resultado_evento_normalizado = resultado_evento.strip().lower()

        # Filtrar apostas vencedoras
        apostas_vencedoras = []
        for aposta in apostas:
            aposta_opcao = aposta['opcao'].strip().lower()
            aposta_resultado = opcao_para_resultado.get(aposta_opcao)
            if aposta_resultado == resultado_evento_normalizado:
                apostas_vencedoras.append(aposta)

        # Calcular o total apostado nas opções vencedoras e no total
        total_apostado = sum([aposta['valor'] for aposta in apostas])
        total_vencedores = sum([aposta['valor'] for aposta in apostas_vencedoras])

        if total_vencedores > 0:
            # Calcular o prêmio para cada usuário
            for aposta in apostas_vencedoras:
                proporcao = aposta['valor'] / total_vencedores
                premio = total_apostado * proporcao * valor_cota

                # Atualizar o saldo do usuário
                carteira = conn.execute('SELECT id FROM carteiras WHERE id_usuario = ?', (aposta['id_usuario'],)).fetchone()
                if carteira:
                    conn.execute('UPDATE carteiras SET saldo = saldo + ? WHERE id = ?', (premio, carteira['id']))
                    # Registrar a transação
                    conn.execute('''
                        INSERT INTO transacoes (id_carteira, tipo, valor, detalhes)
                        VALUES (?, 'credito', ?, ?)
                    ''', (carteira['id'], premio, f'Prêmio do evento {evento_id}'))
        else:
            print("Nenhuma aposta vencedora para este evento.")
    except Exception as e:
        print(f"Erro ao distribuir prêmios: {e}")

def enviar_email_rejeicao(motivo_rejeicao, evento_id):
    """
    Função para enviar um e-mail ao usuário informando sobre a rejeição de um evento.
    """

    with sqlite3.connect(database_path) as conn:
        conn.row_factory = sqlite3.Row
        evento = conn.execute('SELECT id_criador, titulo FROM eventos WHERE id = ?', (evento_id,)).fetchone()
        criador = conn.execute('SELECT email FROM usuarios WHERE id = ?', (evento['id_criador'],)).fetchone()
        if criador and criador['email']:
            email_usuario = criador['email']
        else:
            print("Email do usuário não encontrado.")    
        # Configuração do servidor de e-mail
        smtp_server = 'smtp.gmail.com'
        port = 587
        remetente = 'projetointegradorpython@gmail.com'
        senha = 'vpql ekjt daeh thjk'

        # Configuração da mensagem   
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = email_usuario
        msg['Subject'] = 'Rejeição de Aposta'

        if criador and criador['email']:
            email_usuario = criador['email']

        # Adiciona o corpo da mensagem com UTF-8
        corpo_mensagem = f"Ola, sua aposta '{evento['titulo']}' foi rejeitada pelo seguinte motivo: {motivo_rejeicao}"
        msg.attach(MIMEText(corpo_mensagem, 'plain', 'utf-8'))

        try:
            # Tenta se conectar ao servidor SMTP
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(remetente, senha)

            # Envia o e-mail
            server.sendmail(remetente, email_usuario, msg.as_string())

        except Exception as e:
            print(f"Erro ao enviar email: {e}")
    
        finally:
            # Fecha a conexão com o servidor
            server.quit()


"-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
"criar evento"


@app.route('/criar_evento', methods=['GET', 'POST'])
def criar_evento():
    """
    Lida com a rota '/criar_evento', permitindo que usuários autenticados do tipo 'usuario' criem um novo evento. Suporta métodos GET e POST para exibir e processar o formulário de criação de evento.

    Funcionalidades principais:
    - Verifica se o usuário está autenticado e é do tipo 'usuario'.
    - No método POST:
      - Recupera e valida os dados do formulário (título, descrição, categoria, valor da cota, data do evento).
      - Calcula as datas de início e fim das apostas com base nas datas atuais e do evento.
      - Insere o novo evento e sua categoria no banco de dados.
      - Exibe mensagens de sucesso ou erro ao usuário.
    - No método GET:
      - Carrega as categorias disponíveis para serem exibidas no formulário.

    Retorno:
    - POST bem-sucedido: Redireciona com mensagem de sucesso.
    - Erros de validação: Renderiza o formulário com mensagens de erro.
    - GET: Renderiza o formulário de criação de evento com as categorias disponíveis.
    """
    if 'logged_in' not in session or session['user_type'] != 'usuario':
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Recupera os dados do formulário
        titulo = request.form['titulo'].strip()
        descricao = request.form['descricao'].strip()
        categoria_id = request.form.get('categoria')
        try:
            valor_cota = float(request.form['valor_cota'])
        except ValueError:
            flash("O valor da cota deve ser um número válido.", "error")
            return render_template('criar_evento.html', categorias=carregar_categorias(), form_data=request.form)
        data_evento_str = request.form['data_evento']

        # Validações
        errors = []

        if not titulo or len(titulo) > 50:
            errors.append("O título deve ter entre 1 e 50 caracteres.")
        if not descricao or len(descricao) > 150:
            errors.append("A descrição deve ter entre 1 e 150 caracteres.")
        if valor_cota < 1.00:
            errors.append("O valor da cota deve ser no mínimo R$1,00.")
        if not categoria_id:
            errors.append("Por favor, selecione uma categoria.")

        # Convertendo a string para objeto datetime
        try:
            data_evento = datetime.strptime(data_evento_str, '%Y-%m-%d')
        except ValueError:
            errors.append("Formato de data inválido. Use o formato AAAA-MM-DD.")

        data_atual = datetime.now()

        # Validações de data
        if 'data_evento' in locals():
            if data_evento.date() <= data_atual.date():
                errors.append("A data do evento deve ser posterior à data atual.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template('criar_evento.html', categorias=carregar_categorias(), form_data=request.form)

        # Definir o período de apostas
        data_inicio_apostas = data_atual.date()
        data_fim_apostas = (data_evento - timedelta(days=1)).date()

        # Verificar se o período de apostas é válido
        if data_fim_apostas < data_inicio_apostas:
            flash("A data de término das apostas não pode ser anterior à data de início.", "error")
            return render_template('criar_evento.html', categorias=carregar_categorias(), form_data=request.form)

        # Inserindo os dados na tabela
        try:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()

            user_id = get_user_id()
            if user_id is None:
                flash("Usuário não autenticado ou sessão expirada.", "error")
                return render_template('criar_evento.html', categorias=carregar_categorias(), form_data=request.form)

            # Inserir o evento na tabela 'eventos'
            sql_evento = '''INSERT INTO eventos (titulo, descricao, valor_cota, data_evento, data_inicio_apostas, data_fim_apostas, id_criador)
                            VALUES (?, ?, ?, ?, ?, ?, ?)'''
            evento_values = (
                titulo,
                descricao,
                valor_cota,
                data_evento_str,
                data_inicio_apostas.strftime('%Y-%m-%d'),
                data_fim_apostas.strftime('%Y-%m-%d'),
                user_id
            )
            cursor.execute(sql_evento, evento_values)
            evento_id = cursor.lastrowid  # Obter o ID do evento inserido

            # Inserir o relacionamento na tabela 'eventos_categorias'
            sql_categoria = '''INSERT INTO eventos_categorias (id_evento, id_categoria) VALUES (?, ?)'''
            cursor.execute(sql_categoria, (evento_id, categoria_id))

            conn.commit()
            flash("Evento criado com sucesso!", "success")
            return redirect(url_for('criar_evento'))
        except sqlite3.Error as e:
            error_message = f"Erro ao inserir no banco de dados: {e}"

            flash(error_message, "error")
            return render_template('criar_evento.html', categorias=carregar_categorias(), form_data=request.form)
        finally:
            conn.close()
    else:
        # Carregar categorias da tabela 'categorias_eventos'
        categorias = carregar_categorias()

    # Renderiza o formulário na página, passando as categorias
    return render_template('criar_evento.html', categorias=categorias)

def carregar_categorias():
    """
    Esta função carrega as categorias de eventos do banco de dados para serem exibidas no formulário
    de criação de evento.

    Funcionalidades:
    1. Conecta ao banco de dados e executa uma consulta SQL para obter todas as categorias da tabela
       'categorias_eventos'.
    2. Retorna as categorias em uma lista de tuplas contendo o ID e o nome de cada categoria.

    Retorno:
    - Uma lista de categorias obtidas da tabela 'categorias_eventos'.
    - Se ocorrer um erro ao carregar as categorias, retorna uma lista vazia.
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM categorias_eventos")
        categorias = cursor.fetchall()
    except sqlite3.Error as e:
        categorias = []
        error_message = f"Erro ao carregar categorias: {e}"
    finally:
        conn.close()
    return categorias

"------------------------------- carteira----------------------------------"

@app.route('/gerenciar_carteira')
def gerenciar_carteira():
    """
    Função para gerenciar a carteira de um usuário.

    Esta função lida com as requisições na rota '/gerenciar_carteira'.
    - Verifica se o usuário está logado e obtém o ID do usuário a partir da sessão.
    - Se o ID do usuário for encontrado, conecta-se ao banco de dados SQLite e executa as operações:
      - Obtém o saldo da carteira do usuário.
      - Obtém o histórico de transações e apostas do usuário.
    - Prepara os dados de transações e apostas para serem exibidos no template HTML.
    - Retorna o template 'gerenciar_carteira.html' com o saldo, histórico de transações e apostas.
    - Se o usuário não estiver logado ou o ID não for encontrado, redireciona para a página de login.
    
    Uso: Esta função é chamada quando o usuário deseja visualizar e gerenciar sua carteira.
    """
    if 'logged_in' in session:
        user_id = get_user_id()
        
        if user_id:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()

            # Obter saldo
            cursor.execute('SELECT saldo FROM carteiras WHERE id_usuario = ?', (user_id,))
            result = cursor.fetchone()
            saldo = result[0] if result else 0.00

            # Obter o id da carteira do usuário
            cursor.execute('SELECT id FROM carteiras WHERE id_usuario = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                carteira_id = result[0]
            else:
                carteira_id = None  # Ou lidar com o caso de não existência

            # Obter histórico de transações
            if carteira_id:
                cursor.execute('SELECT data_transacao, tipo, valor, detalhes FROM transacoes WHERE id_carteira = ? ORDER BY data_transacao DESC', (carteira_id,))
                transacoes = cursor.fetchall()
            else:
                transacoes = []

            # Obter histórico de apostas
            cursor.execute('''
                SELECT apostas.data_aposta, eventos.titulo, apostas.valor, apostas.opcao
                FROM apostas
                JOIN eventos ON apostas.id_evento = eventos.id
                WHERE apostas.id_usuario = ?
                ORDER BY apostas.data_aposta DESC
            ''', (user_id,))
            apostas = cursor.fetchall()

            conn.close()

            # Preparar transações para o template
            transacoes_formatadas = []
            for transacao in transacoes:
                transacoes_formatadas.append({
                    'data_transacao': transacao[0],
                    'tipo': transacao[1],
                    'valor': transacao[2],
                    'detalhes': transacao[3],
                })

            # Preparar apostas para o template
            apostas_formatadas = []
            for aposta in apostas:
                apostas_formatadas.append({
                    'data_aposta': aposta[0],
                    'titulo_evento': aposta[1],
                    'valor': aposta[2],
                    'opcao': aposta[3],
                })

            # Obter mensagens flash
            mensagens = get_flashed_messages()

            return render_template('gerenciar_carteira.html', saldo=saldo, transacoes=transacoes_formatadas, apostas=apostas_formatadas, mensagens=mensagens)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

    
@app.route('/adicionar', methods=['POST'])
def carteira_adicionar():
    """
    Função para adicionar créditos à carteira do usuário.

    Esta função lida com as requisições POST na rota '/adicionar'.
    - Verifica se o usuário está logado e obtém o ID do usuário.
    - Recebe o valor a ser adicionado via formulário.
    - Conecta-se ao banco de dados SQLite e verifica se a carteira do usuário existe:
      - Se a carteira existir, atualiza o saldo da carteira.
      - Se a carteira não existir, cria uma nova carteira para o usuário.
    - Registra a transação de adição de créditos.
    - Exibe uma mensagem de sucesso via flash e redireciona o usuário de volta para a página de gerenciamento da carteira.
    
    Uso: Esta função é chamada quando o usuário deseja adicionar créditos à sua carteira.
    """
    if 'logged_in' in session:
        user_id = get_user_id()
        if user_id:
            valor_adicionar = float(request.form['valor_adicionar'])

            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()

            # Verificar se a carteira existe; caso contrário, criar
            cursor.execute('SELECT id FROM carteiras WHERE id_usuario = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                carteira_id = result[0]
                # Atualizar o saldo
                cursor.execute('UPDATE carteiras SET saldo = saldo + ? WHERE id_usuario = ?', (valor_adicionar, user_id))
            else:
                # Criar carteira para o usuário
                cursor.execute('INSERT INTO carteiras (id_usuario, saldo) VALUES (?, ?)', (user_id, valor_adicionar))
                carteira_id = cursor.lastrowid

            # Registrar a transação
            cursor.execute('''
                INSERT INTO transacoes (id_carteira, tipo, valor, detalhes)
                VALUES (?, 'Compra de Créditos', ?, 'Adição de créditos via cartão')
            ''', (carteira_id, valor_adicionar))

            conn.commit()
            conn.close()

            flash('Créditos adicionados com sucesso!')

            return redirect(url_for('gerenciar_carteira'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/sacar', methods=['POST'])
def carteira_sacar():
    """
    Função para realizar o saque de créditos da carteira do usuário.

    Esta função lida com as requisições POST na rota '/sacar'.
    - Verifica se o usuário está logado e obtém o ID do usuário.
    - Recebe o valor e o método de saque via formulário.
    - Aplica as taxas apropriadas com base no valor do saque.
    - Verifica se o saldo do usuário é suficiente para realizar o saque.
    - Deduz o valor total do saldo do usuário.
    - Registra a transação de saque no banco de dados.
    - Exibe uma mensagem de sucesso via flash e redireciona o usuário de volta para a página de gerenciamento da carteira.
    
    Uso: Esta função é chamada quando o usuário deseja realizar um saque da sua carteira.
    """
    if 'logged_in' in session:
        user_id = get_user_id()
        if user_id:
            valor_saque = float(request.form['valor_saque'])
            metodo_saque = request.form['metodo_saque']
            detalhes = ''

            # Limitar o saque a R$ 101.000,00 por transação
            if valor_saque > 101000:
                flash('O valor máximo para saque por transação é R$ 101.000,00.')
                return redirect(url_for('gerenciar_carteira'))

            # Aplicar taxas conforme tabela
            if valor_saque <= 100:
                taxa = 0.04 * valor_saque
            elif valor_saque <= 1000:
                taxa = 0.03 * valor_saque
            elif valor_saque <= 5000:
                taxa = 0.02 * valor_saque
            elif valor_saque <= 100000:
                taxa = 0.01 * valor_saque
            else:
                taxa = 0.00  # Isento

            # O valor total a ser deduzido do saldo é o valor de saque
            valor_total = valor_saque

            # O valor líquido que o usuário receberá é o valor de saque menos a taxa
            valor_liquido = valor_saque - taxa

            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()

            # Verificar se a carteira existe
            cursor.execute('SELECT saldo, id FROM carteiras WHERE id_usuario = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                saldo = result[0]
                carteira_id = result[1]
            else:
                conn.close()
                flash('Erro: Carteira não encontrada.')
                return redirect(url_for('gerenciar_carteira'))

            if valor_total > saldo:
                conn.close()
                flash('Saldo insuficiente para realizar o saque.')
                return redirect(url_for('gerenciar_carteira'))

            # Deduzir o valor total do saldo
            novo_saldo = saldo - valor_total
            cursor.execute('UPDATE carteiras SET saldo = ? WHERE id_usuario = ?', (novo_saldo, user_id))

            # Preparar detalhes do saque
            if metodo_saque == 'banco':
                banco = request.form['banco']
                agencia = request.form['agencia']
                conta = request.form['conta']
                detalhes = f'Saque para Banco: {banco}, Agência: {agencia}, Conta: {conta}'
            elif metodo_saque == 'pix':
                chave_pix = request.form['chave_pix']
                detalhes = f'Saque via PIX para a chave: {chave_pix}'

            detalhes += f' | Taxa aplicada: R$ {taxa:.2f} | Valor líquido: R$ {valor_liquido:.2f}'

            # Registrar a transação
            cursor.execute('''
                INSERT INTO transacoes (id_carteira, tipo, valor, detalhes)
                VALUES (?, 'Saque', ?, ?)
            ''', (carteira_id, -valor_total, detalhes))

            conn.commit()
            conn.close()

            flash('Saque realizado com sucesso!')
            return redirect(url_for('gerenciar_carteira'))
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

def conectar_db():
    # Atualize o caminho do banco de dados se necessário
    return sqlite3.connect('data/database.db')

@app.route('/apostar', methods=['POST'])
def apostar():
    """
    Esta função lida com a rota '/apostar' e permite que um usuário autenticado realize uma aposta em um evento específico. A aposta inclui a seleção de uma opção específica do evento.

    Funcionalidades:
    1. Verifica se o usuário está autenticado através da sessão.
    2. Obtém os dados do formulário: ID do evento, valor da aposta e opção selecionada.
    3. Valida os dados recebidos:
       - Verifica se o valor da aposta é positivo.
       - Verifica se a opção selecionada é válida ('sim' ou 'nao').
    4. Conecta-se ao banco de dados para realizar as seguintes operações:
       - Obtém o valor da cota do evento.
       - Calcula o valor total da aposta multiplicando o valor da aposta pelo valor da cota.
       - Verifica se o usuário possui saldo suficiente na carteira.
       - Insere a aposta no banco de dados incluindo a opção selecionada.
       - Atualiza o saldo da carteira do usuário subtraindo o valor total da aposta.
    5. Retorna uma mensagem de sucesso ou erro ao usuário e redireciona para a área do usuário.

    Uso: Esta função é chamada quando um usuário autenticado envia o formulário de aposta em um evento.

    Retorno:
    - Se a aposta for realizada com sucesso: Exibe uma mensagem de sucesso e redireciona para a área do usuário.
    - Se ocorrer um erro: Exibe uma mensagem de erro e redireciona para a área do usuário.
    - Se o usuário não estiver autenticado: Redireciona para a página de login.
    """
    if 'logged_in' in session:
        user_id = get_user_id()
        evento_id = request.form.get('evento_id')
        valor_aposta_str = request.form.get('valor_aposta')
        opcao = request.form.get('aposta')

        # Validações iniciais
        if not evento_id or not valor_aposta_str or not opcao:
            flash("Dados incompletos no formulário.", "error")
            return redirect(url_for('area_usuario'))

        try:
            valor_aposta = float(valor_aposta_str)
            if valor_aposta <= 0:
                flash("O valor da aposta deve ser positivo.", "error")
                return redirect(url_for('area_usuario'))
        except ValueError:
            flash("Valor da aposta inválido.", "error")
            return redirect(url_for('area_usuario'))

        if opcao not in ['sim', 'nao']:
            flash("Opção de aposta inválida.", "error")
            return redirect(url_for('area_usuario'))

        try:
            # Usar gerenciador de contexto para abrir a conexão
            with sqlite3.connect(database_path, timeout=5) as conn:
                cursor = conn.cursor()
                
                # Obter o valor da cota do evento
                cursor.execute('SELECT valor_cota FROM eventos WHERE id = ?', (evento_id,))
                resultado = cursor.fetchone()

                if resultado is not None:
                    valor_cota = resultado[0]
                    valor_total_aposta = valor_aposta * valor_cota

                    # Verificar o saldo do usuário
                    cursor.execute('SELECT saldo FROM carteiras WHERE id_usuario = ?', (user_id,))
                    saldo_result = cursor.fetchone()

                    if saldo_result is not None:
                        saldo = saldo_result[0]
                        if saldo >= valor_total_aposta:
                            # Inserir a aposta, incluindo a opção
                            cursor.execute('INSERT INTO apostas (id_evento, id_usuario, valor, opcao) VALUES (?, ?, ?, ?)',
                                           (evento_id, user_id, valor_total_aposta, opcao))
                            
                            # Atualizar o saldo da carteira subtraindo o valor total da aposta
                            novo_saldo = saldo - valor_total_aposta
                            cursor.execute('UPDATE carteiras SET saldo = ? WHERE id_usuario = ?', (novo_saldo, user_id))
                            
                            # Registrar a transação
                            cursor.execute('''
                                INSERT INTO transacoes (id_carteira, tipo, valor, detalhes)
                                VALUES ((SELECT id FROM carteiras WHERE id_usuario = ?), 'debito', ?, ?)
                            ''', (user_id, valor_total_aposta, f'Aposta no evento {evento_id}'))

                            # Commit da transação
                            conn.commit()
                            flash("Aposta realizada com sucesso!", "success")
                        else:
                            flash("Saldo insuficiente para realizar a aposta.", "error")
                    else:
                        flash("Carteira não encontrada.", "error")
                else:
                    flash("Evento não encontrado.", "error")
        except Exception as e:
            print(f"Erro ao processar a aposta: {e}")
            flash("Ocorreu um erro ao processar sua aposta. Tente novamente mais tarde.", "error")

        return redirect(url_for('area_usuario'))
    else:
        return redirect(url_for('login'))

def adicionar_premio_na_carteira(id_usuario, valor_premio):
    """
    Esta função adiciona um valor de prêmio à carteira de um usuário específico. Se a carteira não existir, a função pode criar uma nova, dependendo da lógica do sistema.

    Funcionalidades:
    1. Conecta-se ao banco de dados.
    2. Verifica se a carteira do usuário existe:
       - Se existir, atualiza o saldo existente somando o valor do prêmio.
       - Se não existir, cria uma nova carteira para o usuário com o valor do prêmio.
    3. Salva as alterações no banco de dados com um commit.

    Uso: Esta função é chamada quando um usuário ganha um prêmio e o valor precisa ser adicionado à sua carteira.

    Parâmetros:
    - id_usuario: ID do usuário que receberá o prêmio.
    - valor_premio: Valor do prêmio a ser adicionado à carteira do usuário.

    Retorno:
    - Nenhum retorno explícito. A função realiza operações no banco de dados.
    """
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()

        # Verifica se a carteira existe
        cursor.execute('SELECT id FROM carteiras WHERE id_usuario = ?', (id_usuario,))
        result = cursor.fetchone()
        
        if result:
            # Atualiza o saldo existente
            cursor.execute('UPDATE carteiras SET saldo = saldo + ? WHERE id_usuario = ?', (valor_premio, id_usuario))
        else:
            # Caso a carteira não exista, você pode criar uma nova (dependendo da lógica do seu sistema)
            cursor.execute('INSERT INTO carteiras (id_usuario, saldo) VALUES (?, ?)', (id_usuario, valor_premio))

        conn.commit()


if __name__ == '__main__':
    app.run(debug=True)
