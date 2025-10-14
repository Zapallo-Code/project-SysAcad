from django.core.exceptions import ObjectDoesNotExist
from app.models.position_category import PositionCategory


class PositionCategoryRepository:
    @staticmethod
    def create(categoria):
        categoria.save()
        return categoria

    @staticmethod
    def find_by_id(id: int):
        try:
            return PositionCategory.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_all():
        return PositionCategory.objects.all()
    
    @staticmethod
    def update(categoria) -> PositionCategory:
        categoria.save()
        return categoria
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        categoriacargo = PositionCategoryRepository.find_by_id(id)
        if not categoriacargo:
            return False
        categoriacargo.delete()
        return True
    
    @staticmethod
    def find_by_name(name: str):
        return PositionCategory.objects.filter(nombre__icontains=name)

