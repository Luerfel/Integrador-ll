from flask import Flask, request, redirect, url_for, render_template, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secreto'  # Necessário para usar mensagens flash

# Caminho absoluto para o banco de dados
database_path = os.path.join(os.getcwd(), 'data/database.db')

@app.route('/criar_evento', methods=['GET', 'POST'])
def criar_evento():
    if request.method == 'POST':
        # Recupera os dados do formulário
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        valor_cota = float(request.form['valor_cota'])
        data_evento = request.form['data_evento']
        periodo_apostas = request.form['periodo_apostas']
        id_criador = int(request.form['id_criador'])

        # Validações
        if len(titulo) > 50:
            flash("O título deve ter no máximo 50 caracteres.")
            return redirect(url_for('criar_evento'))
        if len(descricao) > 150:
            flash("A descrição deve ter no máximo 150 caracteres.")
            return redirect(url_for('criar_evento'))
        if valor_cota < 1.00:
            flash("O valor da cota deve ser no mínimo R$1,00.")
            return redirect(url_for('criar_evento'))

        # Inserindo os dados na tabela
        try:
            conn = sqlite3.connect(database_path)
            cursor = conn.cursor()
            sql = '''INSERT INTO eventos (titulo, descricao, valor_cota, data_evento, periodo_apostas, id_criador)
                     VALUES (?, ?, ?, ?, ?, ?)'''
            values = (titulo, descricao, valor_cota, data_evento, periodo_apostas, id_criador)
            cursor.execute(sql, values)
            conn.commit()
            flash("Evento criado com sucesso!")
            return redirect(url_for('criar_evento'))
        except sqlite3.Error as e:
            flash(f"Erro ao inserir no banco de dados: {e}")
        finally:
            conn.close()

    # Renderiza o formulário na página
    return render_template('criar_evento.html')

if __name__ == '__main__':
    app.run(debug=True)
