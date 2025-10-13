from dataclasses import dataclass
from app import db
from flask_hashids import HashidMixin

#TODO cambiar a sigal o nombre de libreta_civica, libreta_enrolamiento, pasaporte
@dataclass(init=False, repr=True, eq=True)
class TipoDocumento(HashidMixin,db.Model):
    __tablename__ = 'tipodocumentos'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #sigla: porque pueden tener como L.C, L.E,  
    #nombre: #dni, pasaporte
    dni: int = db.Column(db.Integer, nullable=False)
    libreta_civica: str = db.Column(db.String(20), nullable=False)
    libreta_enrolamiento: str = db.Column(db.String(20), nullable=False)
    pasaporte: str = db.Column(db.String(20), nullable=False)