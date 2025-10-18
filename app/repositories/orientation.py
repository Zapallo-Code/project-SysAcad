from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import Orientation


class OrientationRepository:
    @staticmethod
    def create(orientation_data: Dict[str, Any]) -> Orientation:
        orientation = Orientation(**orientation_data)
        orientation.full_clean()
        orientation.save()
        return orientation

    @staticmethod
    def find_by_id(id: int) -> Optional[Orientation]:
        try:
            return Orientation.objects.select_related(
                "specialty", "plan", "subject"
            ).get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[Orientation]:
        return list(
            Orientation.objects.select_related("specialty", "plan", "subject").all()
        )

    @staticmethod
    def find_by_specialty(specialty_id: int) -> List[Orientation]:
        return list(
            Orientation.objects.filter(specialty_id=specialty_id).select_related(
                "specialty", "plan", "subject"
            )
        )

    @staticmethod
    def find_by_plan(plan_id: int) -> List[Orientation]:
        return list(
            Orientation.objects.filter(plan_id=plan_id).select_related(
                "specialty", "plan", "subject"
            )
        )

    @staticmethod
    def find_by_subject(subject_id: int) -> List[Orientation]:
        return list(
            Orientation.objects.filter(subject_id=subject_id).select_related(
                "specialty", "plan", "subject"
            )
        )

    @staticmethod
    def find_by_name_specialty_plan(
        name: str, specialty_id: int, plan_id: int
    ) -> Optional[Orientation]:
        try:
            return Orientation.objects.select_related(
                "specialty", "plan", "subject"
            ).get(name=name, specialty_id=specialty_id, plan_id=plan_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(orientation: Orientation) -> Orientation:
        orientation.full_clean()
        orientation.save()
        return orientation

    @staticmethod
    def delete_by_id(id: int) -> bool:
        orientation = OrientationRepository.find_by_id(id)
        if not orientation:
            return False
        orientation.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Orientation.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name_specialty_plan(
        name: str, specialty_id: int, plan_id: int
    ) -> bool:
        return Orientation.objects.filter(
            name=name, specialty_id=specialty_id, plan_id=plan_id
        ).exists()

    @staticmethod
    def count() -> int:
        return Orientation.objects.count()

    @staticmethod
    def find_with_full_relations(id: int) -> Optional[Orientation]:
        try:
            return Orientation.objects.select_related(
                "specialty", "specialty__faculty", "plan", "subject"
            ).get(id=id)
        except ObjectDoesNotExist:
            return None
