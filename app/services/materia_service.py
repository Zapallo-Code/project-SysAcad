from app.models import Materia
from app.repositories import MateriaRepository, AutoridadRepository

class MateriaService:
    @staticmethod
    def crear(materia):
       MateriaRepository.crear(materia)

    @staticmethod
    def buscar_por_id(id: int) -> Materia:
        return MateriaRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Materia]:
        return MateriaRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, materia: Materia) -> Materia:
        materia_existente = MateriaRepository.buscar_por_id(id)
        if not materia_existente:
            return None
        materia_existente.nombre = materia.nombre
        materia_existente.codigo = materia.codigo
        materia_existente.observacion = materia.observacion
        return MateriaRepository.actualizar(materia_existente)

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return MateriaRepository.borrar_por_id(id)



    @staticmethod
    def asociar_autoridad(materia_id: int, autoridad_id: int):
        materia = MateriaRepository.buscar_por_id(materia_id)
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        if not materia or not autoridad:
            raise ValueError("Materia o autoridad no encontrada")
        MateriaRepository.asociar_autoridad(materia, autoridad)

    @staticmethod
    def desasociar_autoridad(materia_id: int, autoridad_id: int):
        materia = MateriaRepository.buscar_por_id(materia_id)
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        if not materia or not autoridad:
            raise ValueError("Materia o autoridad no encontrada")
        MateriaRepository.desasociar_autoridad(materia, autoridad)
