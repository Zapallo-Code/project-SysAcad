from app import db
from app.models import Grado

class GradoRepository:
    
    @staticmethod
    def crear(grado):
        db.session.add(grado)
        db.session.commit()
        
    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Grado).filter_by(id=id).first()
    

    @staticmethod
    def buscar_todos():
        return db.session.query(Grado).all()
    

    @staticmethod
    def actualizar(grado) -> Grado:
        db.session.merge(grado)
        db.session.commit()
        return grado 
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        grado = db.session.query(Grado).filter_by(id=id).first()
        if not grado:
            return False
        db.session.delete(grado)
        db.session.commit()
        return True
