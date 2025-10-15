from app.models.department import Department
from app.repositories.department import DepartmentRepository


class DepartmentService:

    @staticmethod
    def create(departament):
        DepartmentRepository.create(departament)

    @staticmethod
    def find_by_id(id: int) -> Department:
        return DepartmentRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Department]:
        return DepartmentRepository.find_all()

    @staticmethod
    def update(id: int, departament: Department) -> Department:
        existing_department = DepartmentRepository.find_by_id(id)
        if not existing_department:
            return None
        existing_department.name = departament.name
        return DepartmentRepository.update(existing_department)

    @staticmethod
    def delete_by_id(id: int) -> bool:
        return DepartmentRepository.delete_by_id(id)
