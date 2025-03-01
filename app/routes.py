from flask import Blueprint, render_template

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return render_template("home.html")

@bp.route("/task")
def task():
    return render_template("task.html")

@bp.route("/goal")
def goal():
    return render_template("goal.html")

@bp.route("/history")
def history():
    return render_template("history.html")
