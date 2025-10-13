from dataclasses import dataclass
from app import db
from app.models import TipoEspecialidad
from flask_hashids import HashidMixin

@dataclass(init=False, repr=True, eq=True)
class Especialidad(HashidMixin,db.Model):
    __tablename__ = 'especialidades'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    letra: str = db.Column(db.String(1), nullable=False)
    observacion:str = db.Column(db.String(255), nullable=True)
    
    tipoespecialidad_id: int = db.Column(db.Integer, db.ForeignKey('tipoespecialidades.id'), nullable=False)
    tipoespecialidad = db.relationship('TipoEspecialidad',  lazy=True)

    facultad_id: int = db.Column(db.Integer, db.ForeignKey('facultades.id'), nullable=False)
    facultad = db.relationship('Facultad', lazy=True)
    #TODO especialidad muchos a uno con facultad