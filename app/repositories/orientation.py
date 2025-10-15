from django.core.exceptions import ObjectDoesNotExist
from app.models.orientation import Orientation


class OrientationRepository:
    @staticmethod
    def create(orientation):
        orientation.save()
        return orientation

    @staticmethod
    def find_by_id(id: int):
        try:
            return Orientation.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Orientation.objects.all()

    @staticmethod
    def update(orientation) -> Orientation:
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
    def find_by_specialty(specialty_id: int):
        return Orientation.objects.filter(specialty_id=specialty_id)

    @staticmethod
    def find_by_plan(plan_id: int):
        return Orientation.objects.filter(plan_id=plan_id)

    @staticmethod
    def find_with_relations(id: int):
        try:
            return Orientation.objects.select_related(
                'specialty', 'plan', 'subject'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None
