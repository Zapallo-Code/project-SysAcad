from app.models.position import Position
from app.repositories.position_repository import PositionRepository

class PositionService:
     
    @staticmethod
    def create(position):
        PositionRepository.create(position)

    @staticmethod
    def find_by_id(id: int) -> Position:        
        return PositionRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Position]:
        return PositionRepository.find_all()
    
    @staticmethod
    def update(id: int, position: Position) -> Position:
        existing_position = PositionRepository.find_by_id(id)
        if not existing_position:
            return None
        existing_position.name = position.name
        existing_position.points = position.points
        existing_position.position_category = position.position_category
        existing_position.dedication_type = position.dedication_type
        return PositionRepository.update(existing_position)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return PositionRepository.delete_by_id(id)

