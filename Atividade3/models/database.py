
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Maker(db.Model):
    __tablename__ = "makers"
    id = db.Column(db.Integer, primary_key=True)
    fabricante = db.Column(db.String(100), nullable=False, unique=True)
    models = db.relationship("Model", backref="maker_ref", lazy=True)

    def __init__(self, fabricante):
        self.fabricante = fabricante


class Model(db.Model):
    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(200), nullable=False)
    modelo = db.Column(db.String(200), nullable=False)
    maker_id = db.Column(db.Integer, db.ForeignKey("makers.id"), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(500), nullable=False)
    

    def __init__(self, marca, modelo, maker_id, ano, image):
        self.marca = marca
        self.modelo = modelo
        self.maker_id = maker_id
        self.ano = ano
        self.image = image
