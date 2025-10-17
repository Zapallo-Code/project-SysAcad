from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from app.models import Position


class PositionRepository:
    @staticmethod
    def create(position: Position) -> Position:
        position.full_clean()
        position.save()
        return position

    @staticmethod
    def find_by_id(id: int) -> Optional[Position]:
        try:
            return Position.objects.select_related(
                'position_category', 'dedication_type'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[Position]:
        return list(Position.objects.select_related(
            'position_category', 'dedication_type'
        ).all())

    @staticmethod
    def find_by_category(position_category_id: int) -> List[Position]:
        return list(Position.objects.filter(
            position_category_id=position_category_id
        ).select_related('position_category', 'dedication_type'))

    @staticmethod
    def find_by_dedication_type(dedication_type_id: int) -> List[Position]:
        return list(Position.objects.filter(
            dedication_type_id=dedication_type_id
        ).select_related('position_category', 'dedication_type'))

    @staticmethod
    def find_by_name(name: str) -> List[Position]:
        return list(Position.objects.filter(
            name__icontains=name
        ).select_related('position_category', 'dedication_type'))

    @staticmethod
    def find_by_points_range(min_points: int, max_points: int) -> List[Position]:
        return list(Position.objects.filter(
            points__gte=min_points,
            points__lte=max_points
        ).select_related('position_category', 'dedication_type'))

    @staticmethod
    def update(position: Position) -> Position:
        position.full_clean()
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
    def exists_by_id(id: int) -> bool:
        return Position.objects.filter(id=id).exists()

    @staticmethod
    def count() -> int:
        return Position.objects.count()

    @staticmethod
    def find_with_relations(id: int) -> Optional[Position]:
        try:
            return Position.objects.select_related(
                'position_category', 'dedication_type'
            ).prefetch_related(
                'authorities'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None
