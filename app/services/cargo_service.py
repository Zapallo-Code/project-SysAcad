from app.models import Cargo
from app.repositories import CargoRepository

class CargoService:
     
    @staticmethod
    def crear(cargo):
        CargoRepository.crear(cargo)

    @staticmethod
    def buscar_por_id(id: int) -> Cargo:        
        return CargoRepository.buscar_por_id(id)

    @staticmethod
    def buscar_todos() -> list[Cargo]:
        return CargoRepository.buscar_todos()
    
    @staticmethod
    def actualizar(id: int, cargo: Cargo) -> Cargo:
        cargo_existente = CargoRepository.buscar_por_id(id)
        if not cargo_existente:
            return None
        cargo_existente.nombre = cargo.nombre
        cargo_existente.puntos = cargo.puntos
        cargo_existente.categoria_cargo = cargo.categoria_cargo
        cargo_existente.tipo_dedicacion = cargo.tipo_dedicacion
        return CargoRepository.actualizar(cargo_existente)
        
    
    @staticmethod
    def borrar_por_id(id: int) -> bool:
        return CargoRepository.borrar_por_id(id)
