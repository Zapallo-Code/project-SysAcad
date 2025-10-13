from app import db
from app.models import Materia, Autoridad

class MateriaRepository:
    @staticmethod
    def crear(materia):
        db.session.add(materia)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Materia).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Materia).all()

    @staticmethod
    def actualizar(materia) -> Materia:
        db.session.merge(materia)
        db.session.commit()
        return materia

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        materia = db.session.query(Materia).filter_by(id=id).first()
        if not materia:
            return False
        db.session.delete(materia)
        db.session.commit()
        return True

    @staticmethod
    def asociar_autoridad(materia: Materia, autoridad: Autoridad):
        materia.asociar_autoridad(autoridad)
        db.session.commit()

    @staticmethod
    def desasociar_autoridad(materia: Materia, autoridad: Autoridad):
        materia.desasociar_autoridad(autoridad)
        db.session.commit()
