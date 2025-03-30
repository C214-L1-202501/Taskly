import pytest

from app import create_app
from app.models import db
from config import TestingConfig


@pytest.fixture
def app():
    """Cria uma instância do app configurada para testes"""
    app = create_app(TestingConfig)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Configura o cliente de teste do Flask"""
    return app.test_client()


def test_create_task(client):
    """Teste para criar uma nova tarefa"""
    response = client.post(
        "/api/tasks",
        json={
            "name": "Testar API",
            "due_date": "2025-03-20",
            "description": "Verificar se o CRUD funciona corretamente",
        },
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Tarefa criada!"
    assert "task" in data


def test_create_task_missing_fields(client):
    """Teste para tentar criar uma tarefa sem campos obrigatórios"""
    response = client.post("/api/tasks", json={"name": "Tarefa description e due date"})

    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Campo(s) obrigatório(s) ausentes: due_date, description"


def test_get_nonexistent_task(client):
    """Teste para tentar obter uma tarefa que não existe"""
    response = client.get("/api/tasks/999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Tarefa não encontrada."


def test_get_nonexistent_task_non_int(client):
    """Teste para tentar obter uma tarefa com um ID inválido não inteiro"""
    response = client.get("/api/tasks/#$%¨&")
    assert response.status_code == 404
    data = response.get_json()
    assert data == None


def test_bulk_task_creation(client):
    """Teste para criar várias tarefas e validar a listagem"""
    tasks_data = [
        {"name": "Tarefa 1", "due_date": "2025-03-20", "description": "Descrição 1"},
        {"name": "Tarefa 2", "due_date": "2025-03-21", "description": "Descrição 2"},
        {"name": "Tarefa 3", "due_date": "2025-03-22", "description": "Descrição 3"},
    ]

    for task in tasks_data:
        response = client.post("/api/tasks", json=task)
        assert response.status_code == 201

    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(tasks_data)


def test_get_task(client):
    """Teste para obter uma tarefa específica"""
    client.post(
        "/api/tasks",
        json={
            "name": "Testar GET ID",
            "due_date": "2025-03-20",
            "description": "Verificar se busca por ID funciona",
        },
    )

    response = client.get("/api/tasks/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Testar GET ID"


def test_update_task(client):
    """Teste para atualizar uma tarefa"""
    client.post(
        "/api/tasks",
        json={
            "name": "Tarefa Antiga",
            "due_date": "2025-03-20",
            "description": "Antes da atualização",
        },
    )

    response = client.put(
        "/api/tasks/1",
        json={"name": "Tarefa Atualizada", "description": "Agora está atualizada"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Tarefa atualizada!"

    response = client.get("/api/tasks/1")
    data = response.get_json()
    assert data["name"] == "Tarefa Atualizada"
    assert data["description"] == "Agora está atualizada"


def test_update_task_nonexistant_field(client):
    """Teste para atualizar uma tarefa, com os nomes dos campos errados"""
    client.post(
        "/api/tasks",
        json={
            "name": "Tarefa Antiga",
            "due_date": "2025-03-20",
            "description": "Antes da atualização",
        },
    )

    response = client.put(
        "/api/tasks/1",
        json={"naame": "Tarefa Atualizada", "desxcription": "Agora está atualizada"},
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["message"] == "Nenhum campo a ser atualizado."


def test_update_task_twice(client):
    """Teste para atualizar uma tarefa duas vezes, a qual o método PUT deve permitir"""
    client.post(
        "/api/tasks",
        json={
            "name": "Tarefa Antiga",
            "due_date": "2025-03-20",
            "description": "Antes da atualização",
        },
    )

    response = client.put(
        "/api/tasks/1",
        json={"name": "Tarefa Atualizada", "description": "Agora está atualizada"},
    )

    response = client.put(
        "/api/tasks/1",
        json={"name": "Tarefa Atualizada", "description": "Agora está atualizada"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Tarefa atualizada!"

    response = client.get("/api/tasks/1")
    data = response.get_json()
    assert data["name"] == "Tarefa Atualizada"
    assert data["description"] == "Agora está atualizada"


def test_delete_task(client):
    """Teste para deletar uma tarefa"""
    client.post(
        "/api/tasks",
        json={
            "name": "Tarefa a Deletar",
            "due_date": "2025-03-20",
            "description": "Será excluída",
        },
    )

    response = client.delete("/api/tasks/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Tarefa deletada!"

    response = client.get("/api/tasks/1")
    assert response.status_code == 404


def test_delete_task_twice(client):
    """Teste para deletar uma tarefa duas vezes"""
    client.post(
        "/api/tasks",
        json={
            "name": "Tarefa a Deletar",
            "due_date": "2025-03-20",
            "description": "Será excluída",
        },
    )

    response = client.delete("/api/tasks/1")

    response = client.delete("/api/tasks/1")
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Tarefa não encontrada."


def test_bulk_task_creation_missing_field(client):
    """Teste para criar várias tarefas e validar a listagem, com uma tarefa sem descrição"""
    tasks_data = [
        {"name": "Tarefa 1", "due_date": "2025-03-20", "description": "Descrição 1"},
        {"name": "Tarefa 2", "due_date": "2025-03-21", "description": "Descrição 2"},
        {"name": "Tarefa 3", "due_date": "2025-03-22"},
    ]

    for task in tasks_data:
        response = client.post("/api/tasks", json=task)
        if "description" not in task:
            data = response.get_json()
            assert data["message"] == "Campo(s) obrigatório(s) ausentes: description"
        else:
            assert response.status_code == 201

    """verifica se a tarefa sem descrição não foi adicionada"""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == len(tasks_data) - 1
