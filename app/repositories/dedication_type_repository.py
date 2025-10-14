from django.core.exceptions import ObjectDoesNotExist
from app.models.dedication_type import DedicationType


class DedicationTypeRepository:
    @staticmethod
    def create(dedication_type):
        dedication_type.save()
        return dedication_type
    
    @staticmethod
    def find_by_id(id: int):
        try:
            return DedicationType.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_all():
        return DedicationType.objects.all()
    
    @staticmethod
    def update(dedication_type) -> DedicationType:
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
    def find_by_name(name: str):
        return DedicationType.objects.filter(nombre__icontains=name)

