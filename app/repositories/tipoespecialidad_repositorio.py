from app import db
from app.models import TipoEspecialidad

class TipoEspecialidadRepository:
    @staticmethod
    def crear(tipoespecialidad):
        db.session.add(tipoespecialidad)
        db.session.commit()
        
    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(TipoEspecialidad).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(TipoEspecialidad).all()

    @staticmethod
    def actualizar(tipoespecialidad) -> TipoEspecialidad:
        db.session.merge(tipoespecialidad)
        db.session.commit()
        return tipoespecialidad
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        tipoespecialidad = db.session.query(TipoEspecialidad).filter_by(id=id).first()
        if not tipoespecialidad:
            return False
        db.session.delete(tipoespecialidad)
        db.session.commit()
        return True
