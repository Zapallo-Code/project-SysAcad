from app.models.university import University
from app.repositories.university import UniversityRepository

class UniversityService:
    @staticmethod
    def create(university: University):
        UniversityRepository.create(university)
    
    @staticmethod
    def find_by_id(id: int) -> University:
        return UniversityRepository.find_by_id(id)
    
    @staticmethod
    def find_all() -> list[University]:
        return UniversityRepository.find_all()
    
    @staticmethod
    def update(id: int, university: University) -> University:
        existing_university = UniversityRepository.find_by_id(id)
        if not existing_university:
            return None
        existing_university.name = university.name
        existing_university.acronym = university.acronym
        return UniversityRepository.update(existing_university)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return UniversityRepository.delete_by_id(id)


    