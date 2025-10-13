from app.models import CategoriaCargo
from app.repositories import CategoriaCargoRepository

class CategoriaCargoService:

    @staticmethod
    def crear(categoria):
        CategoriaCargoRepository.crear(categoria)

    @staticmethod
    def buscar_por_id(id: int) -> CategoriaCargo:
        return CategoriaCargoRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[CategoriaCargo]:
        return CategoriaCargoRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, tipodocumento: CategoriaCargo) -> CategoriaCargo:
        categoria_existente = CategoriaCargoRepository.buscar_por_id(id)
        if not categoria_existente:
            return None
        categoria_existente.nombre = tipodocumento.nombre
        return CategoriaCargoRepository.actualizar(categoria_existente)
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return CategoriaCargoRepository.borrar_por_id(id)
