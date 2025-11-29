from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    concluida = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    imagem = db.Column(db.String(200), nullable=True)  # caminho da imagem

    def __repr__(self):
        return f"<Tarefa {self.titulo}>"