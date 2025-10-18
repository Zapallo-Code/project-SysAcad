import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import DepartmentRepository

logger = logging.getLogger(__name__)


class DepartmentService:
    @staticmethod
    @transaction.atomic
    def create(department_data: dict) -> Any:
        logger.info(f"Creating department: {department_data.get('name')}")

        if DepartmentRepository.exists_by_name(department_data.get("name")):
            logger.error(
                f"Department name {department_data.get('name')} already exists"
            )
            raise ValueError(
                f"Department name '{department_data.get('name')}' is already taken"
            )

        created_department = DepartmentRepository.create(department_data)
        logger.info(f"Department created successfully with id: {created_department.id}")
        return created_department

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding department with id: {id}")
        department = DepartmentRepository.find_by_id(id)
        if not department:
            logger.warning(f"Department with id {id} not found")
        return department

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding department with name: {name}")
        department = DepartmentRepository.find_by_name(name)
        if not department:
            logger.warning(f"Department with name '{name}' not found")
        return department

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all departments")
        departments = DepartmentRepository.find_all()
        logger.info(f"Found {len(departments)} departments")
        return departments

    @staticmethod
    def find_by_faculty(faculty_id: int) -> List[Any]:
        """Find all departments for a specific faculty."""
        logger.info(f"Finding departments for faculty id: {faculty_id}")
        departments = DepartmentRepository.find_by_faculty(faculty_id)
        logger.info(f"Found {len(departments)} departments for faculty {faculty_id}")
        return departments

    @staticmethod
    @transaction.atomic
    def update(id: int, department_data: dict) -> Any:
        logger.info(f"Updating department with id: {id}")

        existing_department = DepartmentRepository.find_by_id(id)
        if not existing_department:
            logger.error(f"Department with id {id} not found for update")
            raise ValueError(f"Department with id {id} does not exist")

        name = department_data.get("name")
        if name and name != existing_department.name:
            if DepartmentRepository.exists_by_name(name):
                logger.error(f"Department name {name} already exists")
                raise ValueError(f"Department name '{name}' is already taken")

        for key, value in department_data.items():
            if hasattr(existing_department, key):
                setattr(existing_department, key, value)

        updated_department = DepartmentRepository.update(existing_department)
        logger.info(f"Department with id {id} updated successfully")
        return updated_department

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting department with id: {id}")

        if not DepartmentRepository.exists_by_id(id):
            logger.error(f"Department with id {id} not found for deletion")
            raise ValueError(f"Department with id {id} does not exist")

        result = DepartmentRepository.delete_by_id(id)
        logger.info(f"Department with id {id} deleted successfully")
        return result

    @staticmethod
    @transaction.atomic
    def delete(id: int) -> bool:
        """Alias for delete_by_id for compatibility."""
        return DepartmentService.delete_by_id(id)
