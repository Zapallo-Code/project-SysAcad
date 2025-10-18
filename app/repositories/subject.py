from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import Subject
from app.models import Authority


class SubjectRepository:
    @staticmethod
    def create(subject_data: Dict[str, Any]) -> Subject:
        subject = Subject(**subject_data)
        subject.full_clean()
        subject.save()
        return subject

    @staticmethod
    def find_by_id(id: int) -> Optional[Subject]:
        try:
            return Subject.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_code(code: str) -> Optional[Subject]:
        try:
            return Subject.objects.get(code=code)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[Subject]:
        return list(Subject.objects.all())

    @staticmethod
    def find_by_name(name: str) -> List[Subject]:
        return list(Subject.objects.filter(name__icontains=name))

    @staticmethod
    def find_by_name_exact(name: str) -> Optional[Subject]:
        try:
            return Subject.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(subject: Subject) -> Subject:
        subject.full_clean()
        subject.save()
        return subject

    @staticmethod
    def delete_by_id(id: int) -> bool:
        subject = SubjectRepository.find_by_id(id)
        if not subject:
            return False
        subject.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Subject.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_code(code: str) -> bool:
        return Subject.objects.filter(code=code).exists()

    @staticmethod
    def count() -> int:
        return Subject.objects.count()

    @staticmethod
    def find_with_relations(id: int) -> Optional[Subject]:
        try:
            return Subject.objects.prefetch_related(
                'authorities',
                'authorities__position',
                'orientations'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def associate_authority(subject: Subject, authority: Authority) -> None:
        authority.subjects.add(subject)

    @staticmethod
    def disassociate_authority(subject: Subject, authority: Authority) -> None:
        authority.subjects.remove(subject)
