from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from app.models import SpecialtyType


class SpecialtyTypeRepository:
    @staticmethod
    def create(specialty_type: SpecialtyType) -> SpecialtyType:
        specialty_type.full_clean()
        specialty_type.save()
        return specialty_type

    @staticmethod
    def find_by_id(id: int) -> Optional[SpecialtyType]:
        try:
            return SpecialtyType.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[SpecialtyType]:
        try:
            return SpecialtyType.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_name(name: str) -> List[SpecialtyType]:
        return list(SpecialtyType.objects.filter(name__icontains=name))

    @staticmethod
    def find_by_level(level: str) -> List[SpecialtyType]:
        return list(SpecialtyType.objects.filter(level__icontains=level))

    @staticmethod
    def find_all() -> List[SpecialtyType]:
        return list(SpecialtyType.objects.all())

    @staticmethod
    def update(specialty_type: SpecialtyType) -> SpecialtyType:
        specialty_type.full_clean()
        specialty_type.save()
        return specialty_type

    @staticmethod
    def delete_by_id(id: int) -> bool:
        specialty_type = SpecialtyTypeRepository.find_by_id(id)
        if not specialty_type:
            return False
        specialty_type.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return SpecialtyType.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return SpecialtyType.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return SpecialtyType.objects.count()
