from flask_sqlalchemy import SQLAlchemy
from models import db 

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Relaciona a tarefa ao usuário
    status = db.Column(db.String(20), default='pendente')

    def to_dict(self):
        return {"id": self.id, "title": self.title, "status": self.status}