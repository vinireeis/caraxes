# Caraxes API  
#### API para gerenciamento de projetos e tarefas.  
___  

## Iniciando o projeto  

Abaixo estão os métodos para execução do serviço via Poetry ou Docker. O método recomendado é o Docker.  

- **Python**: Python 3.12  
- **Docker**: Docker version 27.2.0  
- **Docker Compose**: v2.29.2-desktop.2  

### Observação:  
- O arquivo `.env` foi incluído no repositório para facilitar os testes. **Não é uma boa prática**.  
___  

## Iniciando o projeto com Docker  

Certifique-se de estar no diretório raiz do projeto.  

Execute o comando abaixo para subir os serviços da API e do PostgreSQL:  
```bash  
docker-compose up -d  
```  

Os testes e o alembic irão executar automaticamente com o docker da api e algo semelhante deve aparecer:  
```bash  
 ============================= test session starts ==============================
caraxes-api          | platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0
caraxes-api          | rootdir: /src
caraxes-api          | configfile: pytest.ini
caraxes-api          | testpaths: tests
caraxes-api          | plugins: asyncio-0.24.0, cov-6.0.0, anyio-4.6.2.post1
caraxes-api          | asyncio: mode=Mode.AUTO, default_loop_scope="function"
caraxes-api          | collected 26 items
caraxes-api          |
caraxes-api          | tests/src/services/projects/test_project_service.py ......               [ 23%]
caraxes-api          | tests/src/services/tasks/test_task_service.py ..............             [ 76%]
caraxes-api          | tests/src/services/users/test_user_service.py ......                     [100%]
caraxes-api          |
caraxes-api          | ---------- coverage: platform linux, python 3.12.7-final-0 -----------
caraxes-api          | Name                                Stmts   Miss  Cover   Missing
caraxes-api          | -----------------------------------------------------------------
caraxes-api          | src/services/__init__.py                0      0   100%
caraxes-api          | src/services/projects/__init__.py       0      0   100%
caraxes-api          | src/services/projects/service.py       32      0   100%
caraxes-api          | src/services/tasks/__init__.py          0      0   100%
caraxes-api          | src/services/tasks/service.py          54      0   100%
caraxes-api          | src/services/users/__init__.py          0      0   100%
caraxes-api          | src/services/users/service.py          24      0   100%
caraxes-api          | -----------------------------------------------------------------
caraxes-api          | TOTAL                                 110      0   100%
caraxes-api          |
caraxes-api          |
caraxes-api          | ============================== 26 passed in 0.25s ==============================
caraxes-api          | INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
caraxes-api          | INFO  [alembic.runtime.migration] Will assume transactional DDL.
caraxes-api          | INFO  [alembic.runtime.migration] Running upgrade  -> 88bf4a225e8b, create tables
```  

Verifique se os serviços estão funcionando:  
```bash  
docker-compose ps  
```  

Você verá uma saída semelhante a:  
```bash  
NAME                  IMAGE          COMMAND                  SERVICE   CREATED         STATUS         PORTS  
caraxes-postgres-db   postgres       "docker-entrypoint.s…"   db        1 minute ago    Up 2 seconds   0.0.0.0:5432->5432/tcp  
caraxes-api           caraxes-api    "poetry run python3 …"   api       1 minute ago    Up 2 seconds   0.0.0.0:9000->9000/tcp  
```  
___  

## Iniciando o projeto com Poetry  

### Passo 1  
Instale o Poetry (https://python-poetry.org/docs/).  

### Passo 2  
Entre no diretório raiz do projeto e crie o ambiente virtual:  
```bash  
poetry shell  
```  

### Passo 3  
Instale as dependências:  
```bash  
poetry install  
```  

### Passo 4  
Suba o serviço do PostgreSQL necessário para persistência:  
```bash  
docker-compose up -d db  
```

### Passo 5  
Rode o alembic, para aplicar migration e criar tabelas:  
```bash  
alembic upgrade head
```

### Passo 6  
Inicie a aplicação:  
```bash  
python3 main.py  
```  

Você verá uma saída semelhante:  
```bash  
caraxes-api          | Server is ready at URL 0.0.0.0:9000/caraxes-api
caraxes-api          |                                                      _
caraxes-api          |   ___ __ _ _ __ __ ___  _____  ___        __ _ _ __ (_)
caraxes-api          |  / __/ _` | '__/ _` \ \/ / _ \/ __|_____ / _` | '_ \| |
caraxes-api          | | (_| (_| | | | (_| |>  <  __/\__ \_____| (_| | |_) | |
caraxes-api          |  \___\__,_|_|  \__,_/_/\_\___||___/      \__,_| .__/|_|
caraxes-api          |                                               |_|
caraxes-api          |
caraxes-api          | INFO:     Started server process [12]
caraxes-api          | INFO:     Waiting for application startup.
caraxes-api          | INFO:     Application startup complete.
caraxes-api          | INFO:     Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
```  
___  

## Swagger - Documentação  

Acesse a documentação interativa gerada automaticamente pelo FastAPI no link:  
> [http://localhost:9000/caraxes-api/docs](http://localhost:9000/caraxes-api/docs)  
___  

## Padrão de Resposta  

Todas as respostas da API seguem um padrão consistente, garantindo uma fácil interpretação dos resultados e dos possíveis erros.  

### Estrutura de Resposta  

```json  
{  
  "success": true,  
  "internal_code": 0,  
  "message": "Operação realizada com sucesso",  
  "status_code": 200,  
  "payload": {  
    // Dados específicos da resposta  
  }  
}  
```  

### Descrição dos Campos  

- **success**: Indica o resultado geral da operação.  
  - `true`: A operação foi concluída com sucesso.  
  - `false`: Ocorreu um erro na operação.  

- **internal_code**: Código interno para identificar o tipo de resposta/erro/fluxo.  
  - `0`: Sucesso.  
  - `51`: DataNotFound.
  - Entre outros diversos.

- **message**: Mensagem explicativa sobre o resultado da operação ou para servir o client/front.  
  - Exemplo: `"Operação realizada com sucesso"` ou `"Erro ao processar a solicitação"`.  

- **status_code**: Código HTTP padrão para indicar o estado da requisição.  
  - Exemplo: `200` para sucesso, `400` para erro de validação, etc.  

- **payload**: Dados retornados pela operação.  
  - Pode conter objetos específicos, listas ou informações adicionais dependendo da requisição realizada.  
  - Exemplo para listar usuários:  
    ```json  
    "payload": {  
      "users": [  
        {  
          "id": 1,  
          "name": "John Doe",  
          "email": "john@example.com"  
        }  
      ],  
      "total": 1,  
      "limit": 10,  
      "offset": 0  
    }  
    ```  

### Exemplo de Resposta de Sucesso  
```json  
{  
  "success": true,  
  "internal_code": 0,  
  "message": "New user created successfully",  
  "status_code": 201,  
  "payload": {  
    "id": 1  
  }  
}  
```  

### Exemplo de Resposta de Erro  
```json  
{  
  "success": false,  
  "internal_code": 40,  
  "message": "User not found",  
  "status_code": 404  
}
```

## Endpoints  

### Users  

#### 1. Listar usuários paginados  
- **Rota**: `GET /caraxes-api/users`  
- **Descrição**: Lista usuários com paginação.  

**Parâmetros de consulta**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo |  
|-----------|-----------------|-------------|---------|  
| limit     | Limite de itens | Não         | 10      |  
| offset    | Offset inicial  | Não         | 0       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "payload": {  
    "users": [  
      {  
        "id": 1,  
        "name": "John Doe",  
        "email": "john@example.com",  
        "role": "admin"  
      }  
    ],  
    "total": 1,  
    "limit": 10,  
    "offset": 0  
  }  
}  
```  

#### 2. Criar novo usuário  
- **Rota**: `POST /caraxes-api/users`  
- **Descrição**: Cria um novo usuário.  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição      | Obrigatório | Exemplo          |  
|-----------|----------------|-------------|------------------|  
| name      | Nome do usuário| Sim         | "Jane Doe"       |  
| email     | Email do usuário| Sim        | "jane@example.com"|  
| role      | Função         | Não         | "manager"        |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "New user created successfully",  
  "payload": {  
    "id": 2  
  }  
}  
```  

#### 3. Obter um usuário específico  
- **Rota**: `GET /caraxes-api/users/{user_id}`  
- **Descrição**: Retorna detalhes de um usuário específico.  

**Parâmetro de caminho**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo |  
|-----------|-----------------|-------------|---------|  
| user_id   | ID do usuário   | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "payload": {  
    "id": 1,  
    "name": "John Doe",  
    "email": "john@example.com",  
    "role": "admin"  
  }  
}  
```  

#### 4. Atualizar um usuário  
- **Rota**: `PUT /caraxes-api/users/{user_id}`  
- **Descrição**: Atualiza as informações de um usuário existente.  

**Parâmetro de caminho**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo |  
|-----------|-----------------|-------------|---------|  
| user_id   | ID do usuário   | Sim         | 1       |  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo          |  
|-----------|-----------------|-------------|------------------|  
| name      | Nome do usuário | Sim         | "John Updated"   |  
| email     | Email do usuário| Sim         | "updated@example.com"|  
| role      | Função          | Não         | "manager"        |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "User updated successfully",  
  "payload": {  
    "id": 1  
  }  
}  
```  

#### 5. Deletar um usuário  
- **Rota**: `DELETE /caraxes-api/users/{user_id}`  
- **Descrição**: Deleta um usuário existente.  

**Parâmetro de caminho**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo |  
|-----------|-----------------|-------------|---------|  
| user_id   | ID do usuário   | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "User deleted successfully"  
}  
```  

### Projects  

#### 1. Listar projetos paginados  
- **Rota**: `GET /caraxes-api/projects`  
- **Descrição**: Lista projetos com paginação.  

**Parâmetros de consulta**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo |  
|-----------|-----------------|-------------|---------|  
| limit     | Limite de itens | Não         | 10      |  
| offset    | Offset inicial  | Não         | 0       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "payload": {  
    "projects": [  
      {  
        "id": 1,  
        "name": "Project 1",  
        "status": "PLANNING",  
        "user_id": 1  
      }  
    ],  
    "total": 1,  
    "limit": 10,  
    "offset": 0  
  }  
}  
```  

#### 2. Criar novo projeto  
- **Rota**: `POST /caraxes-api/projects`  
- **Descrição**: Cria um novo projeto.  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo          |  
|-----------|-----------------|-------------|------------------|  
| name      | Nome do projeto | Sim         | "New Project"    |  
| status    | Status do projeto | Sim       | "ACTIVE"         |  
| user_id   | ID do usuário   | Sim         | 1                |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "New project created successfully",  
  "payload": {  
    "id": 2  
  }  
}  
```  

#### 3. Obter um projeto específico  
- **Rota**: `GET /caraxes-api/projects/{project_id}`  
- **Descrição**: Retorna os detalhes de um projeto específico.  

**Parâmetro de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "payload": {  
    "id": 1,  
    "name": "Project 1",  
    "status": "PLANNING",  
    "user_id": 1  
  }  
}  
```  

#### 4. Atualizar um projeto  
- **Rota**: `PUT /caraxes-api/projects/{project_id}`  
- **Descrição**: Atualiza as informações de um projeto existente.  

**Parâmetro de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição        | Obrigatório | Exemplo          |  
|-----------|------------------|-------------|------------------|  
| name      | Nome do projeto  | Sim         | "Updated Project"|  
| status    | Status do projeto| Sim         | "PAUSED"         |  
| user_id   | ID do usuário    | Sim         | 1                |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Project updated successfully",  
  "payload": {  
    "id": 1  
  }  
}  
```  

#### 5. Deletar um projeto  
- **Rota**: `DELETE /caraxes-api/projects/{project_id}`  
- **Descrição**: Deleta um projeto existente.  

**Parâmetro de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Project deleted successfully"  
}  
```  

### Tasks  

#### 1. Listar tarefas paginadas  
- **Rota**: `GET /caraxes-api/projects/tasks`  
- **Descrição**: Lista tarefas com paginação.  

**Parâmetros de consulta**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| limit      | Limite de itens | Não         | 10      |  
| offset     | Offset inicial  | Não         | 0       |  
| project_id | ID do projeto   | Não         | 1       |  
| user_id    | ID do usuário   | Não         | 2       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "payload": {  
    "tasks": [  
      {  
        "id": 1,  
        "project_id": 1,  
        "name": "Task 1",  
        "status": "TODO",  
        "priority": "HIGH"  
      }  
    ],  
    "total": 1,  
    "limit": 10,  
    "offset": 0  
  }  
}  
```  

#### 2. Criar nova tarefa  
- **Rota**: `POST /caraxes-api/projects/{project_id}/tasks`  
- **Descrição**: Cria uma nova tarefa associada a um projeto.  

**Parâmetro de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  

**Parâmetros do corpo da requisição**:  
| Parâmetro     | Descrição       | Obrigatório | Exemplo          |  
|---------------|-----------------|-------------|------------------|  
| name          | Nome da tarefa  | Sim         | "New Task"       |  
| status        | Status da tarefa| Sim         | "TODO"           |  
| priority      | Prioridade      | Não         | "MEDIUM"         |  
| assigned_users| IDs dos usuários atribuídos | Não | [1, 2]         |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "New task created successfully",  
  "payload": {  
    "id": 2  
  }  
}  
```  

#### 3. Obter uma tarefa específica  
- **Rota**: `GET /caraxes-api/projects/{project_id}/tasks/{task_id}`  
- **Descrição**: Retorna os detalhes de uma tarefa específica.  

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  
| task_id    | ID da tarefa    | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "payload": {  
    "id": 1,  
    "project_id": 1,  
    "name": "Task 1",  
    "status": "TODO",  
    "priority": "HIGH",  
    "assigned_users": [1, 2]  
  }  
}  
```  

#### 4. Atualizar uma tarefa  
- **Rota**: `PUT /caraxes-api/projects/{project_id}/tasks/{task_id}`  
- **Descrição**: Atualiza as informações de uma tarefa existente.  

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  
| task_id    | ID da tarefa    | Sim         | 1       |  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição        | Obrigatório | Exemplo          |  
|-----------|------------------|-------------|------------------|  
| name      | Nome da tarefa   | Sim         | "Updated Task"   |  
| status    | Status da tarefa | Sim         | "IN_PROGRESS"    |  
| priority  | Prioridade       | Não         | "LOW"            |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Task updated successfully",  
  "payload": {  
    "id": 1  
  }  
}  
```  

#### 5. Atualizar o status de uma tarefa  
- **Rota**: `PATCH /caraxes-api/projects/{project_id}/tasks/{task_id}/status`  
- **Descrição**: Atualiza o status de uma tarefa.  

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  
| task_id    | ID da tarefa    | Sim         | 1       |  

**Parâmetros do corpo da requisição**:  
| Parâmetro | Descrição       | Obrigatório | Exemplo          |  
|-----------|-----------------|-------------|------------------|  
| status    | Novo status     | Sim         | "DONE"           |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Task status updated successfully",  
  "payload": {  
    "id": 1  
  }  
}  
```  

#### 6. Deletar uma tarefa  
- **Rota**: `DELETE /caraxes-api/projects/{project_id}/tasks/{task_id}`  
- **Descrição**: Deleta uma tarefa existente.  

**Parâmetros de caminho**:  
| Parâmetro  | Descrição       | Obrigatório | Exemplo |  
|------------|-----------------|-------------|---------|  
| project_id | ID do projeto   | Sim         | 1       |  
| task_id    | ID da tarefa    | Sim         | 1       |  

**Resposta**:  
```json  
{  
  "success": true,  
  "message": "Task deleted successfully"  
}  
```  
___  

## HttpStatusCode  

### OK  
- **Código HTTP:** `200 Success`  
- Para requisições bem-sucedidas.  

### Created  
- **Código HTTP:** `201 Created`  
- Para criação de recursos com sucesso.  

### BadRequest  
- **Código HTTP:** `400 Bad Request`  
- Problema na sintaxe ou semântica da requisição.

### UnprocessableContent
- **Código HTTP:** `422 Unprocessable Content`  
- Sintaxe/semântica ok mas fere alguma regra de negócio.  

### InternalServerError  
- **Código HTTP:** `500 Internal Server Error`  
- Erro inesperado no servidor.  
___  
