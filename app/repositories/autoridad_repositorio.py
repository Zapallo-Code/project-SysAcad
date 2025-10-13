from app import db
from app.models import Autoridad, Materia, Facultad

class AutoridadRepository:
    @staticmethod
    def crear(autoridad):
        db.session.add(autoridad)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Autoridad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        return db.session.query(Autoridad).all()

    @staticmethod
    def actualizar(autoridad) -> Autoridad:
        db.session.merge(autoridad)
        db.session.commit()
        return autoridad
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        autoridad = db.session.query(Autoridad).filter_by(id=id).first()
        if not autoridad:
            return False
        db.session.delete(autoridad)
        db.session.commit()
        return True

    @staticmethod
    def asociar_materia(autoridad: Autoridad, materia: Materia):
        autoridad.asociar_materia(materia)
        db.session.commit()

    @staticmethod
    def desasociar_materia(autoridad: Autoridad, materia: Materia):
        autoridad.desasociar_materia(materia)
        db.session.commit()

    @staticmethod
    def asociar_facultad(autoridad: Autoridad, facultad:Facultad):
        autoridad.asociar_facultad(facultad)
        db.session.commit()

    @staticmethod
    def desasociar_facultad(autoridad: Autoridad, facultad: Facultad):
        autoridad.desasociar_facultad(facultad)
        db.session.commit()
