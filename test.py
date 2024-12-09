import pytest
from app import app, itens, salvar_dados
import json
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup_data(client):  
    itens.clear()
    test_data = {
        "1": {
            "id": "1",
            "nome": "Celular",
            "valor": 1200,
            "criado": datetime.now().isoformat(),
            "eletronico": True
        },
        "2": {
            "id": "2",
            "nome": "Livro",
            "valor": 50,
            "criado": datetime.now().isoformat(),
            "eletronico": False
        },
        "3": {
            "id": "3",
            "nome": "Monitor",
            "valor": 800,
            "criado": datetime.now().isoformat(),
            "eletronico": True
        }
    }
    itens.update(test_data)
    try:
        salvar_dados()
        yield test_data  
    finally:
        itens.clear()  
        salvar_dados()

def test_list_items(client, setup_data):
    response = client.get('/api/v1/itens')
    assert response.status_code == 200
    assert len(response.json) == 3

def test_create_item(client, setup_data):  
    data = {
        "nome": "Caderno",
        "valor": 20,
        "eletronico": False
    }
    response = client.post('/api/v1/itens/novo', json=data)
    assert response.status_code == 201
    assert response.json["nome"] == "Caderno"
    assert len(client.get('/api/v1/itens').json) == 4

def test_update_item(client, setup_data):
    update_data = {
        "nome": "iPhone 15",
        "valor": 10.000,
        "eletronico": True  
    }
    response = client.put('/api/v1/itens/alterar/1', json=update_data)
    assert response.status_code == 200
    assert response.json["nome"] == "iPhone 15"

def test_update_invalid_item(client, setup_data):  
    update_data = {
        "nome": "Inexistente",
        "valor": 0,
        "eletronico": False
    }
    response = client.put('/api/v1/itens/alterar/999', json=update_data)
    assert response.status_code == 404

def test_delete_item(client, setup_data):
    initial_count = len(client.get('/api/v1/itens').json)
    response = client.delete('/api/v1/itens/remover/1')
    assert response.status_code == 200
    assert len(client.get('/api/v1/itens').json) == initial_count - 1

def test_delete_invalid_item(client, setup_data):  
    response = client.delete('/api/v1/itens/remover/999')
    assert response.status_code == 404