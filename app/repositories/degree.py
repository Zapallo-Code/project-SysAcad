from django.core.exceptions import ObjectDoesNotExist
from app.models.degree import Degree


class DegreeRepository:
    @staticmethod
    def create(degree):
        degree.save()
        return degree

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
    def update(degree) -> Degree:
        degree.save()
        return degree

    @staticmethod
    def delete_by_id(id: int) -> bool:
        degree = DegreeRepository.find_by_id(id)
        if not degree:
            return False
        degree.delete()
        return True

    @staticmethod
    def find_by_name(name: str):
        return Degree.objects.filter(nombre__icontains=name)
