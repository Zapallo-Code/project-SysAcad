from django.core.exceptions import ObjectDoesNotExist
from app.models.specialty_type import SpecialtyType


class SpecialtyTypeRepository:
    @staticmethod
    def create(specialty_type):
        specialty_type.save()
        return specialty_type

    @staticmethod
    def find_by_id(id: int):
        try:
            return SpecialtyType.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return SpecialtyType.objects.all()

    @staticmethod
    def update(specialty_type) -> SpecialtyType:
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
    def find_by_name(name: str):
        return SpecialtyType.objects.filter(nombre__icontains=name)
