from app.models import Grupo
from app.repositories import GrupoRepository

class GrupoService:
    @staticmethod
    def crear(grupo):
        GrupoRepository.crear(grupo)

    @staticmethod
    def buscar_por_id(id: int) -> Grupo:
        return GrupoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Grupo]:
        return GrupoRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, grupo: Grupo) -> Grupo:
        grupo_existente = GrupoRepository.buscar_por_id(id)
        if not grupo_existente:
            return None
        grupo_existente.nombre = grupo.nombre
        return GrupoRepository.actualizar(grupo_existente)
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return GrupoRepository.borrar_por_id(id)
