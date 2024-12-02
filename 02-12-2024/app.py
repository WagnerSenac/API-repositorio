from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('despesas.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial que exibe as despesas
@app.route('/')
def index():
    conn = get_db_connection()
    despesas = conn.execute('SELECT * FROM despesas').fetchall()
    conn.close()
    return render_template('index.html', despesas=despesas)

# Rota para criar uma nova despesa
@app.route('/adicionar', methods=('GET', 'POST'))
def adicionar():
    if request.method == 'POST':
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        valor = request.form['valor']
        data = request.form['data']

        conn = get_db_connection()
        conn.execute('INSERT INTO despesas (descricao, categoria, valor, data) VALUES (?, ?, ?, ?)',
                     (descricao, categoria, valor, data))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('adicionar.html')

# Rota para editar uma despesa
@app.route('/editar/<int:id>', methods=('GET', 'POST'))
def editar(id):
    conn = get_db_connection()
    despesa = conn.execute('SELECT * FROM despesas WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        valor = request.form['valor']
        data = request.form['data']

        conn.execute('UPDATE despesas SET descricao = ?, categoria = ?, valor = ?, data = ? WHERE id = ?',
                     (descricao, categoria, valor, data, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('editar.html', despesa=despesa)

# Rota para excluir uma despesa
@app.route('/excluir/<int:id>', methods=('GET', 'POST'))
def excluir(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM despesas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)