from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from app.models import Specialty


class SpecialtyRepository:
    @staticmethod
    def create(specialty: Specialty) -> Specialty:
        specialty.full_clean()
        specialty.save()
        return specialty

    @staticmethod
    def find_by_id(id: int) -> Optional[Specialty]:
        try:
            return Specialty.objects.select_related(
                'specialty_type', 'faculty'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[Specialty]:
        return list(Specialty.objects.select_related(
            'specialty_type', 'faculty'
        ).all())

    @staticmethod
    def find_by_faculty(faculty_id: int) -> List[Specialty]:
        return list(Specialty.objects.filter(
            faculty_id=faculty_id
        ).select_related('specialty_type', 'faculty'))

    @staticmethod
    def find_by_letter(letter: str) -> List[Specialty]:
        return list(Specialty.objects.filter(
            letter=letter
        ).select_related('specialty_type', 'faculty'))

    @staticmethod
    def find_by_type(specialty_type_id: int) -> List[Specialty]:
        return list(Specialty.objects.filter(
            specialty_type_id=specialty_type_id
        ).select_related('specialty_type', 'faculty'))

    @staticmethod
    def find_by_letter_and_faculty(letter: str, faculty_id: int) -> Optional[Specialty]:
        try:
            return Specialty.objects.select_related(
                'specialty_type', 'faculty'
            ).get(letter=letter, faculty_id=faculty_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(specialty: Specialty) -> Specialty:
        specialty.full_clean()
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
    def exists_by_id(id: int) -> bool:
        return Specialty.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_letter_and_faculty(letter: str, faculty_id: int) -> bool:
        return Specialty.objects.filter(letter=letter, faculty_id=faculty_id).exists()

    @staticmethod
    def count() -> int:
        return Specialty.objects.count()

    @staticmethod
    def find_with_full_relations(id: int) -> Optional[Specialty]:
        try:
            return Specialty.objects.select_related(
                'specialty_type',
                'faculty',
                'faculty__university'
            ).prefetch_related(
                'students',
                'orientations'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None
