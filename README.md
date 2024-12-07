# TestML - Engineer 

[![Python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)](#)         [![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](#)

## API de Gerenciamento de Itens
### API desenolvida em Python utilizando o framework Flask, ela gerencia objetos seguindo os requisitos:

- Listar itens
- Salvar um novo item
- Alterar um item existente
- Remover um item


### O item possui os seguintes atributos:

- id 
- nome 
- valor 
- criação
- eletrônico


---------------

### Acessar aplicação
https://testeml-engineer-1070410786912.southamerica-east1.run.app

-------------
## Documentação da API

#### Lista todos os itens

```
  GET /api/v1/itens
```
Exemplo de Resposta:
```json
[
  {
    "criado": "07/12/2024 19:51:47",
    "eletronico": false,
    "id": "0",
    "nome": "Alterar",
    "valor": 50
  },
  {
    "criado": "07/12/2024 19:53:58",
    "eletronico": true,
    "id": "1",
    "nome": "Notebook",
    "valor": 4000
  }
]
```


#### Cria um novo item

```
  POST /api/v1/itens/novo
```

Corpo do json:
```json
{
  "nome": "Galaxy S24",
  "valor": 4000.0,
  "eletronico": true,
  "data_criacao": "2024-12-07T10:00:00"
}
```


#### Altera um Item

```
  PUT /api/v1/itens/alterar/<item_id>
```

Corpo do json:
```json
{
  "nome": "Alterar",
  "valor": 50.0,
  "eletronico": false
}
```

#### Deleta um item

```
  DELETE /api/v1/itens/remover/<item_id>
```

Exemplo de Resposta:
```json
{
    "message": "Item deletado com sucesso"
}
```
