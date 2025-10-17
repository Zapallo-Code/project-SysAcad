from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from app.models import Degree


class DegreeRepository:
    @staticmethod
    def create(degree: Degree) -> Degree:
        degree.full_clean()
        degree.save()
        return degree

    @staticmethod
    def find_by_id(id: int) -> Optional[Degree]:
        try:
            return Degree.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[Degree]:
        try:
            return Degree.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_name(name: str) -> List[Degree]:
        return list(Degree.objects.filter(name__icontains=name))

    @staticmethod
    def find_all() -> List[Degree]:
        return list(Degree.objects.all())

    @staticmethod
    def update(degree: Degree) -> Degree:
        degree.full_clean()
        degree.save()
        return degree

    @staticmethod
    def delete_by_id(id: int) -> bool:
        degree = DegreeRepository.find_by_id(id)
        if not degree:
            return False
        degree.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Degree.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return Degree.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return Degree.objects.count()
