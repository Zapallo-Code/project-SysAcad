from django.core.exceptions import ObjectDoesNotExist
from app.models.degree import Degree


class DegreeRepository:
    @staticmethod
    def create(grado):
        grado.save()
        return grado
        
    @staticmethod
    def find_by_id(id: int):
        try:
            return Degree.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_all():
        return Degree.objects.all()
    
    @staticmethod
    def update(grado) -> Degree:
        grado.save()
        return grado 
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        grado = DegreeRepository.find_by_id(id)
        if not grado:
            return False
        grado.delete()
        return True
    
    @staticmethod
    def find_by_name(name: str):
        return Degree.objects.filter(nombre__icontains=name)

