from dataclasses import dataclass
from datetime import date
from app import db
from flask_hashids import HashidMixin


@dataclass(init=False, repr=True, eq=True)
class Plan(HashidMixin, db.Model):
    __tablename__ = "planes"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(50),nullable =False)
    fecha_inicio: date = db.Column(db.Date, nullable=False)
    fecha_fin: date = db.Column(db.Date, nullable=False)
    observacion: str = db.Column(db.String(255), nullable=True)
    

