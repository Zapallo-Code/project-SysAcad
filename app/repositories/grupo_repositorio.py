from app import db
from app.models import Grupo

class GrupoRepository:
    
    @staticmethod
    def crear(grupo):
        db.session.add(grupo)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(Grupo).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(Grupo).all()
    
    @staticmethod
    def actualizar(grupo) -> Grupo:
        db.session.merge(grupo)
        db.session.commit()
        return grupo
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        grupo = db.session.query(Grupo).filter_by(id=id).first()
        if not grupo:
            return False
        db.session.delete(grupo)
        db.session.commit()
        return True
