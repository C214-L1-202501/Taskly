from flask import Blueprint, render_template

bp = Blueprint("main", __name__)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/tasks")
def tasks():
    return render_template("tasks.html")
