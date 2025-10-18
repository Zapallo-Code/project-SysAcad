import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import SpecialtyRepository
from app.repositories import SpecialtyTypeRepository
from app.repositories import FacultyRepository

logger = logging.getLogger(__name__)


class SpecialtyService:

    @staticmethod
    @transaction.atomic
    def create(specialty_data: dict) -> Any:
        logger.info(f"Creating specialty: {specialty_data.get('name')}")

        specialty_type_id = specialty_data.get('specialty_type_id')
        faculty_id = specialty_data.get('faculty_id')

        if SpecialtyRepository.exists_by_name_and_type(
            specialty_data.get('name'), specialty_type_id
        ):
            logger.error(f"Specialty with name {specialty_data.get('name')} and type {specialty_type_id} already exists")
            raise ValueError(f"Specialty with this name and type already exists")

        if specialty_type_id and not SpecialtyTypeRepository.exists_by_id(specialty_type_id):
            logger.error(f"Specialty type with id {specialty_type_id} not found")
            raise ValueError(f"Specialty type with id {specialty_type_id} does not exist")

        if faculty_id and not FacultyRepository.exists_by_id(faculty_id):
            logger.error(f"Faculty with id {faculty_id} not found")
            raise ValueError(f"Faculty with id {faculty_id} does not exist")

        created_specialty = SpecialtyRepository.create(specialty_data)
        logger.info(f"Specialty created successfully with id: {created_specialty.id}")
        return created_specialty

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding specialty with id: {id}")
        specialty = SpecialtyRepository.find_by_id(id)
        if not specialty:
            logger.warning(f"Specialty with id {id} not found")
        return specialty

    @staticmethod
    def find_by_name(name: str) -> List[Any]:
        logger.info(f"Finding specialties with name: {name}")
        specialties = SpecialtyRepository.find_by_name(name)
        logger.info(f"Found {len(specialties)} specialties with name '{name}'")
        return specialties

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all specialties")
        specialties = SpecialtyRepository.find_all()
        logger.info(f"Found {len(specialties)} specialties")
        return specialties

    @staticmethod
    def find_by_faculty(faculty_id: int) -> List[Any]:
        logger.info(f"Finding specialties by faculty id: {faculty_id}")

        if not FacultyRepository.exists_by_id(faculty_id):
            logger.error(f"Faculty with id {faculty_id} not found")
            raise ValueError(f"Faculty with id {faculty_id} does not exist")

        specialties = SpecialtyRepository.find_by_faculty(faculty_id)
        logger.info(f"Found {len(specialties)} specialties for faculty {faculty_id}")
        return specialties

    @staticmethod
    @transaction.atomic
    def update(id: int, specialty_data: dict) -> Any:
        logger.info(f"Updating specialty with id: {id}")

        existing_specialty = SpecialtyRepository.find_by_id(id)
        if not existing_specialty:
            logger.error(f"Specialty with id {id} not found for update")
            raise ValueError(f"Specialty with id {id} does not exist")

        name = specialty_data.get('name')
        specialty_type_id = specialty_data.get('specialty_type_id')

        if name or specialty_type_id:
            check_name = name if name else existing_specialty.name
            check_type = specialty_type_id if specialty_type_id else existing_specialty.specialty_type_id

            if (check_name != existing_specialty.name or check_type != existing_specialty.specialty_type_id):
                if SpecialtyRepository.exists_by_name_and_type(check_name, check_type):
                    logger.error(f"Specialty with name {check_name} and type {check_type} already exists")
                    raise ValueError(f"Specialty with this name and type already exists")

        if specialty_type_id and not SpecialtyTypeRepository.exists_by_id(specialty_type_id):
            logger.error(f"Specialty type with id {specialty_type_id} not found")
            raise ValueError(f"Specialty type with id {specialty_type_id} does not exist")

        faculty_id = specialty_data.get('faculty_id')
        if faculty_id and not FacultyRepository.exists_by_id(faculty_id):
            logger.error(f"Faculty with id {faculty_id} not found")
            raise ValueError(f"Faculty with id {faculty_id} does not exist")

        for key, value in specialty_data.items():
            if hasattr(existing_specialty, key):
                setattr(existing_specialty, key, value)

        updated_specialty = SpecialtyRepository.update(existing_specialty)
        logger.info(f"Specialty with id {id} updated successfully")
        return updated_specialty

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting specialty with id: {id}")

        if not SpecialtyRepository.exists_by_id(id):
            logger.error(f"Specialty with id {id} not found for deletion")
            raise ValueError(f"Specialty with id {id} does not exist")

        result = SpecialtyRepository.delete_by_id(id)
        logger.info(f"Specialty with id {id} deleted successfully")
        return result
