from app.models import Autoridad
from app.repositories import AutoridadRepository, MateriaRepository,FacultadRepository
from app import db

class AutoridadService:
    @staticmethod
    def crear(autoridad):
        AutoridadRepository.crear(autoridad)

    @staticmethod
    def buscar_por_id(id: int) -> Autoridad:
         return AutoridadRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Autoridad]:
       return AutoridadRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, autoridad: Autoridad) -> Autoridad:
        autoridad_existente = AutoridadRepository.buscar_por_id(id)
        if not autoridad_existente:
            return None
        autoridad_existente.nombre = autoridad.nombre
        autoridad_existente.telefono = autoridad.telefono
        autoridad_existente.email = autoridad.email
        return AutoridadRepository.actualizar(autoridad_existente)

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return AutoridadRepository.borrar_por_id(id)

    @staticmethod
    def asociar_materia(autoridad_id: int, materia_id: int):
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        materia = MateriaRepository.buscar_por_id(materia_id)
        if not autoridad or not materia:
            raise ValueError("Materia o autoridad no encontrada")
        AutoridadRepository.asociar_materia(autoridad, materia)

    @staticmethod
    def desasociar_materia(autoridad_id: int, materia_id: int):
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        materia = MateriaRepository.buscar_por_id(materia_id)
        if not autoridad or not materia:
            raise ValueError("Materia o autoridad no encontrada")
        AutoridadRepository.desasociar_materia(autoridad, materia)
        


    @staticmethod
    def asociar_facultad(autoridad_id: int, facultad_id: int):
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        facultad = FacultadRepository.buscar_por_id(facultad_id)
        if not autoridad or not facultad:
            raise ValueError("Facultad o autoridad no encontrada")
        AutoridadRepository.asociar_facultad(autoridad, facultad)

    @staticmethod
    def desasociar_facultad(autoridad_id: int, facultad_id: int):
        autoridad = AutoridadRepository.buscar_por_id(autoridad_id)
        facultad = FacultadRepository.buscar_por_id(facultad_id)
        if not autoridad or not facultad:
            raise ValueError("Facultad o autoridad no encontrada")
        AutoridadRepository.desasociar_facultad(autoridad, facultad)
