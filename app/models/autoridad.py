from dataclasses import dataclass
from app.models import Cargo
from app.models.relations import autoridades_materias , facultades_autoridades
from app import db
from flask_hashids import HashidMixin

@dataclass(init=False, repr=True, eq=True)
class Autoridad(HashidMixin,db.Model):
    __tablename__ = "autoridades"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    telefono: str = db.Column(db.String(20), nullable=True)
    email: str = db.Column(db.String(100), nullable=True)

    cargo_id: int = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    cargo = db.relationship('Cargo',  lazy=True) 

    materias = db.relationship('Materia', secondary=autoridades_materias, back_populates='autoridades')

    facultades = db.relationship('Facultad', secondary=facultades_autoridades, back_populates='autoridades')


    def asociar_materia(self, materia):
        if materia not in self.materias:
            self.materias.append(materia)

    def desasociar_materia(self, materia):
        if materia in self.materias:
            self.materias.remove(materia)

    def asociar_facultad(self, facultad):
        if facultad not in self.facultades:
            self.facultades.append(facultad)
            
    def desasociar_facultad(self, facultad):
        if facultad in self.facultades:
            self.facultades.remove(facultad)