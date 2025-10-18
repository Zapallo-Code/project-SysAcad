from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import Authority
from app.models import Subject
from app.models import Faculty


class AuthorityRepository:
    @staticmethod
    def create(authority_data: Dict[str, Any]) -> Authority:
        authority = Authority(**authority_data)
        authority.full_clean()
        authority.save()
        return authority

    @staticmethod
    def find_by_id(id: int) -> Optional[Authority]:
        try:
            return Authority.objects.select_related("position").get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[Authority]:
        return list(Authority.objects.select_related("position").all())

    @staticmethod
    def find_by_position(position_id: int) -> List[Authority]:
        return list(
            Authority.objects.filter(position_id=position_id).select_related("position")
        )

    @staticmethod
    def find_by_name(name: str) -> List[Authority]:
        return list(
            Authority.objects.filter(name__icontains=name).select_related("position")
        )

    @staticmethod
    def search_by_name(name: str) -> List[Authority]:
        """Search authorities by first name or last name."""
        return list(
            Authority.objects.filter(
                first_name__icontains=name
            ) | Authority.objects.filter(
                last_name__icontains=name
            ).select_related("position")
        )

    @staticmethod
    def find_by_faculty(faculty_id: int) -> List[Authority]:
        """Find all authorities associated with a specific faculty."""
        return list(
            Authority.objects.filter(faculties__id=faculty_id).select_related("position").distinct()
        )

    @staticmethod
    def find_by_email(email: str) -> Optional[Authority]:
        try:
            return Authority.objects.select_related("position").get(email=email)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(authority: Authority) -> Authority:
        authority.full_clean()
        authority.save()
        return authority

    @staticmethod
    def delete_by_id(id: int) -> bool:
        authority = AuthorityRepository.find_by_id(id)
        if not authority:
            return False
        authority.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Authority.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_email(email: str) -> bool:
        return Authority.objects.filter(email=email).exists()

    @staticmethod
    def count() -> int:
        return Authority.objects.count()

    @staticmethod
    def find_with_relations(id: int) -> Optional[Authority]:
        try:
            return (
                Authority.objects.select_related(
                    "position",
                    "position__position_category",
                    "position__dedication_type",
                )
                .prefetch_related("subjects", "faculties", "faculties__university")
                .get(id=id)
            )
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def associate_subject(authority: Authority, subject: Subject) -> None:
        authority.subjects.add(subject)

    @staticmethod
    def disassociate_subject(authority: Authority, subject: Subject) -> None:
        authority.subjects.remove(subject)

    @staticmethod
    def associate_faculty(authority: Authority, faculty: Faculty) -> None:
        authority.faculties.add(faculty)

    @staticmethod
    def disassociate_faculty(authority: Authority, faculty: Faculty) -> None:
        authority.faculties.remove(faculty)
