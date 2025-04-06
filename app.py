from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('controleDeGastos.db')
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/despesas', methods=['POST'])

def add_despesa():
    data = request.get_json()
    descricao = data['descricao']
    valor = data['valor']
    data_despesa = data['data']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO despesas (descricao, valor, data)
        VALUES (?, ?, ?)
    ''', (descricao, valor, data_despesa))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Despesa adicionada com sucesso!'}), 201

@app.route('/despesas', methods=['GET'])
def get_despesas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM despesas')
    despesas = cursor.fetchall()
    despesaslist = [{'id': row[0], 'descricao': row[1], 'valor': row[2], 'data': row[3]} for row in despesas]
    conn.close()

    return jsonify(despesaslist), 200

@app.route('/despesas/<int:id>', methods=['PUT'])

def update_despesa(id): 
    data = request.get_json()
    descricao = data['descricao']
    valor = data['valor']
    data_despesa = data['data']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE despesas
        SET descricao = ?, valor = ?, data = ?
        WHERE id = ?
    ''', (descricao, valor, data_despesa, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Despesa atualizada com sucesso!'}), 200

@app.route('/despesas/<int:id>', methods=['DELETE'])
def delete_despesa(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM despesas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Despesa deletada com sucesso!'}), 200

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
