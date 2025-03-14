from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(1024), nullable=False)

    def __repr__(self):
        return f"<Task - {self.name}>"
