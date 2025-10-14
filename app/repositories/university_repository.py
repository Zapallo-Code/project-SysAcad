from django.core.exceptions import ObjectDoesNotExist
from app.models.university import University


class UniversityRepository:
    @staticmethod
    def create(university):
        university.save()
        return university

    @staticmethod
    def find_by_id(id: int):
        try:
            return University.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return University.objects.all()
    
    @staticmethod
    def update(university) -> University:
        university.save()
        return university
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        university = UniversityRepository.find_by_id(id)
        if not university:
            return False
        university.delete()
        return True
    
    @staticmethod
    def find_by_acronym(acronym: str):
        try:
            return University.objects.get(acronym=acronym)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_with_relations(id: int):
        try:
            return University.objects.prefetch_related('faculties').get(id=id)
        except ObjectDoesNotExist:
            return None

