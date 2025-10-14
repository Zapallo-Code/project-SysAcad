from app.models.orientation import Orientation
from app.repositories.orientation_repository import OrientationRepository

class OrientationService:
    @staticmethod
    def create(orientation):
        OrientationRepository.create(orientation)

    @staticmethod
    def find_by_id(id: int) -> Orientation:        
        return OrientationRepository.find_by_id(id)
    
    @staticmethod
    def find_all() -> list[Orientation]:
        return OrientationRepository.find_all()
    
    @staticmethod
    def update(id: int, orientation: Orientation) -> Orientation:
        existing_orientation = OrientationRepository.find_by_id(id)
        if not existing_orientation:
            return None
        existing_orientation.name = orientation.name
        existing_orientation.specialty_id = orientation.specialty_id
        existing_orientation.plan = orientation.plan
        existing_orientation.subject = orientation.subject
        return OrientationRepository.update(existing_orientation)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return OrientationRepository.delete_by_id(id)

