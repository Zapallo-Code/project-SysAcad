from app import db
from app.models import Orientacion
 
class OrientacionRepository:
    @staticmethod
    def crear(orientacion):
        db.session.add(orientacion)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Orientacion).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(Orientacion).all()
    
    @staticmethod
    def actualizar(orientacion) -> Orientacion:
        db.session.merge(orientacion)
        db.session.commit()
        return orientacion
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        orientacion = db.session.query(Orientacion).filter_by(id=id).first()
        if not orientacion:
            return False
        db.session.delete(orientacion)
        db.session.commit()
        return True
