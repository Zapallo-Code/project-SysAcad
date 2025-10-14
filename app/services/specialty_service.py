from app.models.specialty import Specialty
from app.repositories.specialty_repository import SpecialtyRepository

class SpecialtyService:

    @staticmethod
    def create(specialty):
        SpecialtyRepository.create(specialty)

    @staticmethod
    def find_by_id(id: int) -> Specialty:
        return SpecialtyRepository.find_by_id(id)
    
    @staticmethod
    def find_all() -> list[Specialty]:
        return SpecialtyRepository.find_all()

    @staticmethod
    def update(id: int, specialty: Specialty) -> Specialty:
        existing_specialty = SpecialtyRepository.find_by_id(id)
        if not existing_specialty:
            return None
        existing_specialty.name = specialty.name
        existing_specialty.letter = specialty.letter
        existing_specialty.observation = specialty.observation
        existing_specialty.specialty_type = specialty.specialty_type
        existing_specialty.faculty = specialty.faculty
        return SpecialtyRepository.update(existing_specialty)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return SpecialtyRepository.delete_by_id(id)

