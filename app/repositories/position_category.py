from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import PositionCategory


class PositionCategoryRepository:
    @staticmethod
    def create(position_category_data: Dict[str, Any]) -> PositionCategory:
        position_category = PositionCategory(**position_category_data)
        position_category.full_clean()
        position_category.save()
        return position_category

    @staticmethod
    def find_by_id(id: int) -> Optional[PositionCategory]:
        try:
            return PositionCategory.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[PositionCategory]:
        try:
            return PositionCategory.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_name(name: str) -> List[PositionCategory]:
        return list(PositionCategory.objects.filter(name__icontains=name))

    @staticmethod
    def find_all() -> List[PositionCategory]:
        return list(PositionCategory.objects.all())

    @staticmethod
    def update(position_category: PositionCategory) -> PositionCategory:
        position_category.full_clean()
        position_category.save()
        return position_category

    @staticmethod
    def delete_by_id(id: int) -> bool:
        position_category = PositionCategoryRepository.find_by_id(id)
        if not position_category:
            return False
        position_category.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return PositionCategory.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return PositionCategory.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return PositionCategory.objects.count()
