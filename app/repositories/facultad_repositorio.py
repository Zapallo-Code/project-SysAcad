from app import db
from app.models import Facultad,Autoridad

class FacultadRepository:
    
    @staticmethod
    def crear(facultad):
        db.session.add(facultad)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Facultad).filter_by(id=id).first() 

    @staticmethod
    def buscar_todos():
        return db.session.query(Facultad).all()
    
    @staticmethod
    def actualizar(facultad) -> Facultad:
        db.session.merge(facultad)
        db.session.commit()
        return facultad
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        facultad = db.session.query(Facultad).filter_by(id=id).first()
        if not facultad:
            return False
        db.session.delete(facultad)
        db.session.commit()
        return True
    
    @staticmethod
    def asociar_autoridad(facultad: Facultad, autoridad: Autoridad):
        facultad.asociar_autoridad(autoridad)
        db.session.commit()

    @staticmethod
    def desasociar_autoridad(facultad: Facultad, autoridad: Autoridad):
        facultad.desasociar_autoridad(autoridad)
        db.session.commit()
