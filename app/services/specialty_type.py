import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import SpecialtyTypeRepository

logger = logging.getLogger(__name__)


class SpecialtyTypeService:
    @staticmethod
    @transaction.atomic
    def create(specialty_type_data: dict) -> Any:
        logger.info(f"Creating specialty type: {specialty_type_data.get('name')}")

        if SpecialtyTypeRepository.exists_by_name(specialty_type_data.get("name")):
            logger.error(
                f"Specialty type name {specialty_type_data.get('name')} already exists"
            )
            raise ValueError(
                f"Specialty type name '{specialty_type_data.get('name')}' is already taken"
            )

        created_specialty_type = SpecialtyTypeRepository.create(specialty_type_data)
        logger.info(
            f"Specialty type created successfully with id: {created_specialty_type.id}"
        )
        return created_specialty_type

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding specialty type with id: {id}")
        specialty_type = SpecialtyTypeRepository.find_by_id(id)
        if not specialty_type:
            logger.warning(f"Specialty type with id {id} not found")
        return specialty_type

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding specialty type with name: {name}")
        specialty_type = SpecialtyTypeRepository.find_by_name(name)
        if not specialty_type:
            logger.warning(f"Specialty type with name '{name}' not found")
        return specialty_type

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all specialty types")
        specialty_types = SpecialtyTypeRepository.find_all()
        logger.info(f"Found {len(specialty_types)} specialty types")
        return specialty_types

    @staticmethod
    @transaction.atomic
    def update(id: int, specialty_type_data: dict) -> Any:
        logger.info(f"Updating specialty type with id: {id}")

        existing_specialty_type = SpecialtyTypeRepository.find_by_id(id)
        if not existing_specialty_type:
            logger.error(f"Specialty type with id {id} not found for update")
            raise ValueError(f"Specialty type with id {id} does not exist")

        name = specialty_type_data.get("name")
        if name and name != existing_specialty_type.name:
            if SpecialtyTypeRepository.exists_by_name(name):
                logger.error(f"Specialty type name {name} already exists")
                raise ValueError(f"Specialty type name '{name}' is already taken")

        for key, value in specialty_type_data.items():
            if hasattr(existing_specialty_type, key):
                setattr(existing_specialty_type, key, value)

        updated_specialty_type = SpecialtyTypeRepository.update(existing_specialty_type)
        logger.info(f"Specialty type with id {id} updated successfully")
        return updated_specialty_type

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting specialty type with id: {id}")

        if not SpecialtyTypeRepository.exists_by_id(id):
            logger.error(f"Specialty type with id {id} not found for deletion")
            raise ValueError(f"Specialty type with id {id} does not exist")

        result = SpecialtyTypeRepository.delete_by_id(id)
        logger.info(f"Specialty type with id {id} deleted successfully")
        return result
