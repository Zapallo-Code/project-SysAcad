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
    def find_by_faculty(faculty_id: int) -> List[Department]:
        """Find all departments for a specific faculty."""
        return list(Department.objects.filter(faculty_id=faculty_id).select_related("faculty"))

    @staticmethod
    def update(department: Department) -> Department:
        department.full_clean()
        department.save()
        return department
    
    @staticmethod
    def delete(id: int) -> bool:
        """Delete a department by ID."""
        department = DepartmentRepository.find_by_id(id)
        if not department:
            return False
        department.delete()
        return True

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
    def exists_by_name(name: str, faculty_id: int = None) -> bool:
        """Check if department exists by name, optionally scoped to a faculty."""
        query = Department.objects.filter(name=name)
        if faculty_id is not None:
            query = query.filter(faculty_id=faculty_id)
        return query.exists()

    @staticmethod
    def count() -> int:
        return Department.objects.count()
