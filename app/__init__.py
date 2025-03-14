from flask import Flask

from app.api import api_bp
from app.models import db
from app.routes import bp
from config import STATIC_FOLDER, TEMPLATE_FOLDER, ProductionConfig


def create_app(config_class=ProductionConfig):
    app = Flask(__name__, template_folder=TEMPLATE_FOLDER, static_folder=STATIC_FOLDER)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(bp)
    app.register_blueprint(api_bp, url_prefix="/api")  # API separada

    return app
