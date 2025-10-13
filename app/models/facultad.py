from dataclasses import dataclass
from app import db
from app.models.relations import facultades_autoridades
from flask_hashids import HashidMixin


@dataclass(init=False, repr=True, eq=True)
class Facultad(HashidMixin, db.Model):
    __tablename__ = 'facultades'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(100), nullable=False)
    abreviatura: str = db.Column(db.String(10), nullable=False)
    directorio: str = db.Column(db.String(100), nullable=False)
    sigla: str = db.Column(db.String(10), nullable=False)
    codigopostal: str = db.Column(db.String(10), nullable=True)
    ciudad: str = db.Column(db.String(50), nullable=True)
    domicilio: str = db.Column(db.String(100), nullable=True)
    telefono: str = db.Column(db.String(20), nullable=True)
    contacto: str = db.Column(db.String(100), nullable=True)
    email: str = db.Column(db.String(100), nullable=False)

    universidad_id: int = db.Column(
        db.Integer, db.ForeignKey('universidades.id'), nullable=False)
    universidad = db.relationship('Universidad', lazy=True)

    autoridades = db.relationship(
        'Autoridad', secondary=facultades_autoridades, back_populates='facultades')

    def asociar_autoridad(self, autoridad):
        if autoridad not in self.autoridades:
            self.autoridades.append(autoridad)

    def desasociar_autoridad(self, autoridad):
        if autoridad in self.autoridades:
            self.autoridades.remove(autoridad)
