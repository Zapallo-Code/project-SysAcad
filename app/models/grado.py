from dataclasses import dataclass 
from app import db
from flask_hashids import HashidMixin

@dataclass(init=False, repr=True, eq=True)
class Grado(HashidMixin,db.Model):
    __tablename__ = 'grados'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(50), nullable=False)
    descripcion: str = db.Column(db.String(200), nullable=False)
    


    