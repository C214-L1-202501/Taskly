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
