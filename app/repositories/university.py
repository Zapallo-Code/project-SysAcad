from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from app.models.university import University


class UniversityRepository:
    @staticmethod
    def create(university: University) -> University:
        university.full_clean()
        university.save()
        return university

    @staticmethod
    def find_by_id(id: int) -> Optional[University]:
        try:
            return University.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_acronym(acronym: str) -> Optional[University]:
        try:
            return University.objects.get(acronym=acronym)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[University]:
        try:
            return University.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[University]:
        return list(University.objects.all())

    @staticmethod
    def search_by_name(name: str) -> List[University]:
        return list(University.objects.filter(name__icontains=name))

    @staticmethod
    def update(university: University) -> University:
        university.full_clean()
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
    def exists_by_id(id: int) -> bool:
        return University.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_acronym(acronym: str) -> bool:
        return University.objects.filter(acronym=acronym).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return University.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return University.objects.count()

    @staticmethod
    def find_with_relations(id: int) -> Optional[University]:
        try:
            return University.objects.prefetch_related(
                'faculties',
                'faculties__specialties'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None
