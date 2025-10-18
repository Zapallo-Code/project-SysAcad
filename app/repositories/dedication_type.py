from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import DedicationType


class DedicationTypeRepository:
    @staticmethod
    def create(dedication_type_data: Dict[str, Any]) -> DedicationType:
        dedication_type = DedicationType(**dedication_type_data)
        dedication_type.full_clean()
        dedication_type.save()
        return dedication_type

    @staticmethod
    def find_by_id(id: int) -> Optional[DedicationType]:
        try:
            return DedicationType.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[DedicationType]:
        try:
            return DedicationType.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_name(name: str) -> List[DedicationType]:
        return list(DedicationType.objects.filter(name__icontains=name))

    @staticmethod
    def find_all() -> List[DedicationType]:
        return list(DedicationType.objects.all())

    @staticmethod
    def update(dedication_type: DedicationType) -> DedicationType:
        dedication_type.full_clean()
        dedication_type.save()
        return dedication_type

    @staticmethod
    def delete_by_id(id: int) -> bool:
        dedication_type = DedicationTypeRepository.find_by_id(id)
        if not dedication_type:
            return False
        dedication_type.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return DedicationType.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return DedicationType.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return DedicationType.objects.count()
