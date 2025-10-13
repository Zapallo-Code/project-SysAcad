from app.models import Grado
from app.repositories import GradoRepository


class GradoService:

    @staticmethod
    def crear(grado: Grado):
        GradoRepository.crear(grado)

    @staticmethod
    def buscar_por_id(id: int) -> Grado:
        return GradoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Grado]:
        return GradoRepository.buscar_todos()

    @staticmethod
    def actualizar(id: int, grado: Grado) -> Grado:
        grado_existente = GradoRepository.buscar_por_id(grado.id)
        if not grado_existente:
            return None
        grado_existente.nombre = grado.nombre
        grado_existente.descripcion = grado.descripcion
        return GradoRepository.actualizar(grado_existente)

    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return GradoRepository.borrar_por_id(id)
