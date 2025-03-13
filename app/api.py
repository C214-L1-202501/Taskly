from datetime import datetime

from flask import Blueprint, jsonify, request

from app.models import Tasks, db

api_bp = Blueprint("api", __name__)


@api_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    required_fields = ["name", "due_date", "description"]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        print(f"Campos obrigatórios ausentes: {', '.join(missing_fields)}")
        return (
            jsonify(
                {
                    "message": f"Campo(s) obrigatório(s) ausentes: {', '.join(missing_fields)}"
                }
            ),
            400,
        )

    try:
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        new_task = Tasks(
            name=data["name"], due_date=due_date, description=data["description"]
        )
        db.session.add(new_task)
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "Tarefa criada!",
                    "task": {"id": new_task.id, "name": new_task.name},
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@api_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Tasks.query.all()
    tasks_list = [
        {
            "id": task.id,
            "name": task.name,
            "due_date": task.due_date.strftime("%Y-%m-%d"),
            "description": task.description,
        }
        for task in tasks
    ]
    return jsonify(tasks_list)


@api_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = db.session.get(Tasks, task_id)
    if not task:
        return jsonify({"message": "Tarefa não encontrada."}), 404
    return jsonify(
        {
            "id": task.id,
            "name": task.name,
            "due_date": task.due_date.strftime("%Y-%m-%d"),
            "description": task.description,
        }
    )


@api_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = db.session.get(Tasks, task_id)
    if not task:
        return jsonify({"message": "Tarefa não encontrada."}), 404

    data = request.get_json()
    if "name" in data:
        task.name = data["name"]
    if "due_date" in data:
        try:
            task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Formato de data inválido. Use YYYY-MM-DD"}), 400
    if "description" in data:
        task.description = data["description"]

    db.session.commit()
    return jsonify(
        {"message": "Tarefa atualizada!", "task": {"id": task.id, "name": task.name}}
    )


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Tasks, task_id)
    if not task:
        return jsonify({"message": "Tarefa não encontrada."}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarefa deletada!"})
