from app import db
from app.models import Area

class AreaRepository:
    @staticmethod
    def crear(area):
        db.session.add(area)
        db.session.commit()
    
    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Area).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(Area).all()
    
    @staticmethod
    def actualizar(area) -> Area:
        db.session.merge(area)
        db.session.commit()
        return area
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        area = db.session.query(Area).filter_by(id=id).first()
        if not area:
            return False
        db.session.delete(area)
        db.session.commit()
        return True
