from app.models.position_category import PositionCategory
from app.repositories.position_category_repository import PositionCategoryRepository

class PositionCategoryService:

    @staticmethod
    def create(categoria):
        PositionCategoryRepository.create(categoria)

    @staticmethod
    def find_by_id(id: int) -> PositionCategory:
        return PositionCategoryRepository.find_by_id(id)
    
    @staticmethod
    def find_all() -> list[PositionCategory]:
        return PositionCategoryRepository.find_all()
    
    @staticmethod
    def update(id: int, document_type: PositionCategory) -> PositionCategory:
        categoria_existente = PositionCategoryRepository.find_by_id(id)
        if not categoria_existente:
            return None
        categoria_existente.name = document_type.name
        return PositionCategoryRepository.update(categoria_existente)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return PositionCategoryRepository.delete_by_id(id)

