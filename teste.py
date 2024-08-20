from flask import Flask, send_from_directory

app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def home():
    return send_from_directory('templates', 'index.html')

# Rota para a página de cadastro
@app.route('/cadastro')
def cadastro():
    return send_from_directory('templates', 'cadastro.html')

# Servir arquivos estáticos (CSS, JS, imagens)
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
