from django.core.exceptions import ObjectDoesNotExist
from app.models.department import Department


class DepartmentRepository:
    @staticmethod
    def create(departament):
        departament.save()
        return departament

    @staticmethod
    def find_by_id(id: int):
        try:
            return Department.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Department.objects.all()

    @staticmethod
    def update(departament) -> Department:
        departament.save()
        return departament

    @staticmethod
    def delete_by_id(id: int) -> bool:
        departament = DepartmentRepository.find_by_id(id)
        if not departament:
            return False
        departament.delete()
        return True

    @staticmethod
    def find_by_name(name: str):
        return Department.objects.filter(nombre__icontains=name)
