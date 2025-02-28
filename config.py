import os

BASEDIR = os.path.dirname(os.path.abspath("main.py"))

STATIC_FOLDER = "static"
TEMPLATE_FOLDER = "templates"

class Config:
    FLASK_DEBUG = 1
    SESSION_TYPE = 'filesystem'
