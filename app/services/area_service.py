from app.models import Area
from app.repositories import AreaRepository

class AreaService:
    @staticmethod
    def crear(area):
        AreaRepository.crear(area)
    
    @staticmethod
    def buscar_por_id(id: int) -> Area:
       return AreaRepository.buscar_por_id(id)
    
    @staticmethod
    def buscar_todos() -> list[Area]:
       return AreaRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, area: Area) -> Area:
        area_existente = AreaRepository.buscar_por_id(id)
        if not area_existente:
            return None
        area_existente.nombre = area.nombre
        return AreaRepository.actualizar(area_existente)
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return AreaRepository.borrar_por_id(id)
    
