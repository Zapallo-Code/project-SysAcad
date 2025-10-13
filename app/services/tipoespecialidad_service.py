from app.models import TipoEspecialidad
from app.repositories import TipoEspecialidadRepository



class TipoEspecialidadService:
    @staticmethod
    def crear(tipoespecialidad):
        TipoEspecialidadRepository.crear(tipoespecialidad)
    
    @staticmethod
    def buscar_por_id(id: int) -> TipoEspecialidad:
        return TipoEspecialidadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[TipoEspecialidad]:
        return TipoEspecialidadRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, tipoespecialidad: TipoEspecialidad) -> TipoEspecialidad:
        tipoespecialidad_existente = TipoEspecialidadRepository.buscar_por_id(id)
        if not tipoespecialidad_existente:
            return None
        tipoespecialidad_existente.nombre = tipoespecialidad.nombre
        return TipoEspecialidadRepository.actualizar(tipoespecialidad_existente)
    

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return TipoEspecialidadRepository.borrar_por_id(id)
