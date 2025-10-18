from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import Faculty
from app.models import Authority


class FacultyRepository:
    @staticmethod
    def create(faculty_data: Dict[str, Any]) -> Faculty:
        faculty = Faculty(**faculty_data)
        faculty.full_clean()
        faculty.save()
        return faculty

    @staticmethod
    def find_by_id(id: int) -> Optional[Faculty]:
        try:
            return Faculty.objects.select_related("university").get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_acronym(acronym: str) -> Optional[Faculty]:
        try:
            return Faculty.objects.select_related("university").get(acronym=acronym)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[Faculty]:
        return list(Faculty.objects.select_related("university").all())

    @staticmethod
    def find_by_university(university_id: int) -> List[Faculty]:
        return list(
            Faculty.objects.filter(university_id=university_id).select_related(
                "university"
            )
        )

    @staticmethod
    def find_by_city(city: str) -> List[Faculty]:
        return list(
            Faculty.objects.filter(city__iexact=city).select_related("university")
        )

    @staticmethod
    def update(faculty: Faculty) -> Faculty:
        faculty.full_clean()
        faculty.save()
        return faculty

    @staticmethod
    def delete_by_id(id: int) -> bool:
        faculty = FacultyRepository.find_by_id(id)
        if not faculty:
            return False
        faculty.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Faculty.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_acronym(acronym: str) -> bool:
        return Faculty.objects.filter(acronym=acronym).exists()

    @staticmethod
    def count() -> int:
        return Faculty.objects.count()

    @staticmethod
    def find_with_full_relations(id: int) -> Optional[Faculty]:
        try:
            return (
                Faculty.objects.select_related("university")
                .prefetch_related(
                    "authorities",
                    "authorities__position",
                    "specialties",
                    "specialties__specialty_type",
                )
                .get(id=id)
            )
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def associate_authority(faculty: Faculty, authority: Authority) -> None:
        authority.faculties.add(faculty)

    @staticmethod
    def disassociate_authority(faculty: Faculty, authority: Authority) -> None:
        authority.faculties.remove(faculty)
