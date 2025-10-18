from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import Department


class DepartmentRepository:
    @staticmethod
    def create(department_data: Dict[str, Any]) -> Department:
        department = Department(**department_data)
        department.full_clean()
        department.save()
        return department

    @staticmethod
    def find_by_id(id: int) -> Optional[Department]:
        try:
            return Department.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[Department]:
        try:
            return Department.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_name(name: str) -> List[Department]:
        return list(Department.objects.filter(name__icontains=name))

    @staticmethod
    def find_all() -> List[Department]:
        return list(Department.objects.all())

    @staticmethod
    def update(department: Department) -> Department:
        department.full_clean()
        department.save()
        return department

    @staticmethod
    def delete_by_id(id: int) -> bool:
        department = DepartmentRepository.find_by_id(id)
        if not department:
            return False
        department.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Department.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return Department.objects.filter(name=name).exists()

    @staticmethod
    def count() -> int:
        return Department.objects.count()
