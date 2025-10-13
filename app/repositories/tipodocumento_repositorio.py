from app import db
from app.models import TipoDocumento

class TipoDocumentoRepository:

    @staticmethod
    def crear(tipodocumento):
        db.session.add(tipodocumento)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(TipoDocumento).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(TipoDocumento).all()
    
    @staticmethod
    def actualizar(tipodocumento) -> TipoDocumento:
        db.session.merge(tipodocumento)
        db.session.commit()
        return tipodocumento
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        tipodocumento = db.session.query(TipoDocumento).filter_by(id=id).first()
        if not tipodocumento:
            return False
        db.session.delete(tipodocumento)
        db.session.commit()
        return True
        
