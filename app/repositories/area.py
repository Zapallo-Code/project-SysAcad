from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from app.models import Area


class AreaRepository:
    @staticmethod
    def create(area: Area) -> Area:
        area.full_clean()
        area.save()
        return area

    @staticmethod
    def find_by_id(id: int) -> Optional[Area]:
        try:
            return Area.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[Area]:
        try:
            return Area.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_name(name: str) -> List[Area]:
        return list(Area.objects.filter(name__icontains=name))

    @staticmethod
    def find_all() -> List[Area]:
        return list(Area.objects.all())

    @staticmethod
    def update(area: Area) -> Area:
        area.full_clean()
        area.save()
        return area

    @staticmethod
    def delete_by_id(id: int) -> bool:
        area = AreaRepository.find_by_id(id)
        if not area:
            return False
        area.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Area.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return Area.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return Area.objects.count()
