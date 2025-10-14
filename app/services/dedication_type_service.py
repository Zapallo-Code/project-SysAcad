from app.models.dedication_type import DedicationType
from app.repositories.dedication_type_repository import DedicationTypeRepository

class DedicationTypeService:

    @staticmethod
    def create(dedication_type):
        return DedicationTypeRepository.create(dedication_type)
    
    @staticmethod
    def find_by_id(id: int) -> DedicationType:
        return DedicationTypeRepository.find_by_id(id)
    
    @staticmethod
    def find_all() -> list[DedicationType]:
        return DedicationTypeRepository.find_all()
    
    @staticmethod
    def update(id: int, dedication_type: DedicationType) -> DedicationType:
        dedication_type_existente = DedicationTypeRepository.find_by_id(id)
        if not dedication_type_existente:
            return None
        dedication_type_existente.name = dedication_type.name
        dedication_type_existente.observation = dedication_type.observation
        return DedicationTypeRepository.update(dedication_type_existente)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return DedicationTypeRepository.delete_by_id(id)

    
