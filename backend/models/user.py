# models.py (ou onde você definiu seus modelos)
from flask_sqlalchemy import SQLAlchemy
from . import db 
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # Definição da tabela e colunas
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')  # Método especificado aqui

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)