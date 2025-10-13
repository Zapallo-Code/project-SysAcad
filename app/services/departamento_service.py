from app.models import Departamento
from app.repositories import DepartamentoRepository

class DepartamentoService:

    @staticmethod
    def crear(departamento):
        DepartamentoRepository.crear(departamento)

    @staticmethod
    def buscar_por_id(id: int) -> Departamento:
        return DepartamentoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Departamento]:
         return DepartamentoRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, departamento: Departamento) -> Departamento:
        departamento_existente = DepartamentoRepository.buscar_por_id(id)
        if not departamento_existente:
            return None
        departamento_existente.nombre = departamento.nombre
        return DepartamentoRepository.actualizar(departamento_existente)
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return DepartamentoRepository.borrar_por_id(id)
