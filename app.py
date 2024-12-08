from flask import Flask, request, jsonify, abort
from datetime import datetime
import json
import uuid
import os

app = Flask(__name__)


DB_FILE_PATH = "database.json"

try:
    with open(DB_FILE_PATH, 'r') as file:
        dados = json.load(file)
        itens = {str(i): item for i, item in enumerate(dados)} if isinstance(dados, list) else dados
except FileNotFoundError:
    itens = {}

def salvar_dados():
    with open(DB_FILE_PATH, 'w') as file:
        json.dump(itens, file, indent=4)

def validar_item(data):
    if not all(key in data for key in ['nome', 'valor', 'eletronico']):
        abort(400, description="Campos obrigatórios ausentes")
    if not isinstance(data['valor'], (int, float)) or data['valor'] < 0:
        abort(400, description="Valor inválido")
    if not isinstance(data['eletronico'], bool):
        abort(400, description="Campo 'eletronico' deve ser booleano")

@app.route('/api/v1/itens', methods=['GET'])
def listar_itens():
    formatted_itens = []
    for item in itens.values():
        formatted_itens.append({
            'id': item['id'],
            'nome': item['nome'],
            'valor': item['valor'],
            'eletronico': item['eletronico'],
            'criado': item['criado']
        })
    return jsonify(formatted_itens), 200

@app.route('/api/v1/itens/novo', methods=['POST'])
def criar_item():
    try:
        data = request.json
        validar_item(data)
        
        next_id = str(max(map(int, itens.keys()), default=-1) + 1)
        item = {
            'id': next_id,
            'nome': data['nome'],
            'valor': data['valor'],
            'eletronico': data['eletronico'],
            'criado': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        itens[next_id] = item
        salvar_dados()
        return jsonify(item), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/v1/itens/alterar/<item_id>', methods=['PUT'])
def atualizar_item(item_id):
    try:
        if item_id not in itens:
            return jsonify({'error': 'Item não encontrado'}), 404
        
        data = request.json
        validar_item(data)
        
        itens[item_id].update({
            'nome': data['nome'],
            'valor': data['valor'],
            'eletronico': data['eletronico']
        })
        
        salvar_dados()
        return jsonify(itens[item_id]), 200
    except KeyError:
        return jsonify({'error': 'Item não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/itens/remover/<item_id>', methods=['DELETE'])
def deletar_item(item_id):
    try:
        if item_id not in itens:
            return jsonify({'error': 'Item não encontrado'}), 404
        
        del itens[item_id]
        salvar_dados()
        return jsonify({'message': 'Item deletado com sucesso'}), 200
    except KeyError:
        return jsonify({'error': 'Item não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Item não encontrado'}), 404

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'error': str(error.description)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    
    port = int(os.environ.get('PORT', 8080))
    
    app.run(host='0.0.0.0', port=port)