from dataclasses import dataclass
from app.models.relations import autoridades_materias
from app import db

@dataclass(init=False, repr=True, eq=True)
class Materia(db.Model):
    __tablename__ = "materias"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(255), nullable=False)
    codigo: str = db.Column(db.String(20), nullable=False)
    observacion: str = db.Column(db.String(255), nullable=True)

    autoridades = db.relationship('Autoridad', secondary =autoridades_materias, back_populates = 'materias')

    def asociar_autoridad(self, autoridad):
        if autoridad not in self.autoridades:
            self.autoridades.append(autoridad)

    def desasociar_autoridad(self, autoridad):
        if autoridad in self.autoridades:
            self.autoridades.remove(autoridad)
