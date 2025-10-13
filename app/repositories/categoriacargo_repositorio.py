from app import db
from app.models import CategoriaCargo

class CategoriaCargoRepository:

    @staticmethod
    def crear(categoria):
        db.session.add(categoria)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        return db.session.query(CategoriaCargo).filter_by(id=id).first()
    
    @staticmethod
    def buscar_todos():
        return db.session.query(CategoriaCargo).all()
    
    @staticmethod
    def actualizar(categoria) -> CategoriaCargo:
        db.session.merge(categoria)
        db.session.commit()
        return categoria
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        categoriacargo = db.session.query(CategoriaCargo).filter_by(id=id).first()
        if not categoriacargo:
            return False
        db.session.delete(categoriacargo)
        db.session.commit()
        return True
