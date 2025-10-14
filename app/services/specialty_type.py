from app.models.specialty_type import SpecialtyType
from app.repositories.specialty_type import SpecialtyTypeRepository


class SpecialtyTypeService:
    @staticmethod
    def create(specialty_type):
        SpecialtyTypeRepository.create(specialty_type)

    @staticmethod
    def find_by_id(id: int) -> SpecialtyType:
        return SpecialtyTypeRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[SpecialtyType]:
        return SpecialtyTypeRepository.find_all()

    @staticmethod
    def update(id: int, specialty_type: SpecialtyType) -> SpecialtyType:
        existing_specialty_type = SpecialtyTypeRepository.find_by_id(id)
        if not existing_specialty_type:
            return None
        existing_specialty_type.name = specialty_type.name
        existing_specialty_type.level = specialty_type.level
        return SpecialtyTypeRepository.update(existing_specialty_type)

    @staticmethod
    def delete_by_id(id: int) -> bool:
        return SpecialtyTypeRepository.delete_by_id(id)
