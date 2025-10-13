from dataclasses import dataclass
from app.models import CategoriaCargo, TipoDedicacion
from app import db
from flask_hashids import HashidMixin

@dataclass(init=False, repr=True, eq=True)
class Cargo(HashidMixin, db.Model):
    __tablename__ = 'cargos'
    id :int = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre: str = db.Column(db.String(50), nullable=False)
    puntos: int = db.Column(db.Integer, nullable = True)
    
    categoria_cargo_id: int = db.Column(db.Integer, db.ForeignKey('categoriacargos.id'), nullable=False)
    categoria_cargo = db.relationship('CategoriaCargo', lazy=True)
    
    tipo_dedicacion_id: int = db.Column(db.Integer, db.ForeignKey('tipodedicaciones.id'), nullable=False)
    tipo_dedicacion = db.relationship('TipoDedicacion', lazy=True)