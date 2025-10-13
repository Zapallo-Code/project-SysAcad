from app import db
from app.models import Universidad

class UniversidadRepository:
    """
    Repositorio para gestionar las universidades.
    """
    @staticmethod
    def crear(universidad):
        """
        Crea una nueva universidad en la base de datos.
        :param universidad: Universidad a crear.
        :return: Universidad creada.
        """
        db.session.add(universidad)
        db.session.commit()

    @staticmethod
    def buscar_por_id(id: int):
        """
        Busca una universidad por su ID.
        :param id: ID de la universidad a buscar.
        :return: Universidad encontrada o None si no existe.
        """
        return db.session.query(Universidad).filter_by(id=id).first()

    @staticmethod
    def buscar_todos():
        """
        Busca todas las universidades en la base de datos.
        :return: Lista de universidades.
        """
        return db.session.query(Universidad).all()
    
    @staticmethod
    def actualizar(universidad) -> Universidad:
        """
        Actualiza una universidad existente en la base de datos.
        :param id: ID de la universidad a actualizar.
        :param universidad: Universidad con los nuevos datos.
        :return: Universidad actualizada.
        """
        db.session.merge(universidad)
        db.session.commit()
        return universidad
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        """
        Borra una universidad por su ID.
        :param id: ID de la universidad a borrar.
        :return: True si fue eliminada, False si no existe.
        """
        universidad = db.session.query(Universidad).filter_by(id=id).first()
        if not universidad:
            return False
        db.session.delete(universidad)
        db.session.commit()
        return True
