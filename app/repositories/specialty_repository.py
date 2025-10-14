from django.core.exceptions import ObjectDoesNotExist
from app.models.specialty import Specialty


class SpecialtyRepository:
    @staticmethod
    def create(specialty):
        specialty.save()
        return specialty

    @staticmethod
    def find_by_id(id: int):
        try:
            return Specialty.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Specialty.objects.all()

    @staticmethod
    def update(specialty) -> Specialty:
        specialty.save()
        return specialty
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        specialty = SpecialtyRepository.find_by_id(id)
        if not specialty:
            return False
        specialty.delete()
        return True
    
    @staticmethod
    def find_by_faculty(faculty_id: int):
        return Specialty.objects.filter(faculty_id=faculty_id)
    
    @staticmethod
    def find_by_letter(letter: str):
        return Specialty.objects.filter(letter=letter)
    
    @staticmethod
    def find_with_relations(id: int):
        try:
            return Specialty.objects.select_related(
                'specialty_type', 'faculty'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None


