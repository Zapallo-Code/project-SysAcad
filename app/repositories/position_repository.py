from django.core.exceptions import ObjectDoesNotExist
from app.models.position import Position


class PositionRepository:
    @staticmethod
    def create(position):
        position.save()
        return position

    @staticmethod
    def find_by_id(id: int):
        try:
            return Position.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_all():
        return Position.objects.all()
    
    @staticmethod
    def update(position) -> Position:
        position.save()
        return position
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        position = PositionRepository.find_by_id(id)
        if not position:
            return False
        position.delete()
        return True
    
    @staticmethod
    def find_by_category(position_category_id: int):
        return Position.objects.filter(position_category_id=position_category_id)
    
    @staticmethod
    def find_with_relations(id: int):
        try:
            return Position.objects.select_related(
                'position_category', 'dedication_type'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None

