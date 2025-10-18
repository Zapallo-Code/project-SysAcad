import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import DedicationTypeRepository

logger = logging.getLogger(__name__)


class DedicationTypeService:
    @staticmethod
    @transaction.atomic
    def create(dedication_type_data: dict) -> Any:
        logger.info(f"Creating dedication type: {dedication_type_data.get('name')}")

        if DedicationTypeRepository.exists_by_name(dedication_type_data.get("name")):
            logger.error(
                f"Dedication type name {dedication_type_data.get('name')} already exists"
            )
            raise ValueError(
                f"Dedication type name '{dedication_type_data.get('name')}' is already taken"
            )

        created_dedication_type = DedicationTypeRepository.create(dedication_type_data)
        logger.info(
            f"Dedication type created successfully with id: {created_dedication_type.id}"
        )
        return created_dedication_type

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding dedication type with id: {id}")
        dedication_type = DedicationTypeRepository.find_by_id(id)
        if not dedication_type:
            logger.warning(f"Dedication type with id {id} not found")
        return dedication_type

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding dedication type with name: {name}")
        dedication_type = DedicationTypeRepository.find_by_name(name)
        if not dedication_type:
            logger.warning(f"Dedication type with name '{name}' not found")
        return dedication_type

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all dedication types")
        dedication_types = DedicationTypeRepository.find_all()
        logger.info(f"Found {len(dedication_types)} dedication types")
        return dedication_types

    @staticmethod
    @transaction.atomic
    def update(id: int, dedication_type_data: dict) -> Any:
        logger.info(f"Updating dedication type with id: {id}")

        existing_dedication_type = DedicationTypeRepository.find_by_id(id)
        if not existing_dedication_type:
            logger.error(f"Dedication type with id {id} not found for update")
            raise ValueError(f"Dedication type with id {id} does not exist")

        name = dedication_type_data.get("name")
        if name and name != existing_dedication_type.name:
            if DedicationTypeRepository.exists_by_name(name):
                logger.error(f"Dedication type name {name} already exists")
                raise ValueError(f"Dedication type name '{name}' is already taken")

        for key, value in dedication_type_data.items():
            if hasattr(existing_dedication_type, key):
                setattr(existing_dedication_type, key, value)

        updated_dedication_type = DedicationTypeRepository.update(
            existing_dedication_type
        )
        logger.info(f"Dedication type with id {id} updated successfully")
        return updated_dedication_type

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting dedication type with id: {id}")

        if not DedicationTypeRepository.exists_by_id(id):
            logger.error(f"Dedication type with id {id} not found for deletion")
            raise ValueError(f"Dedication type with id {id} does not exist")

        result = DedicationTypeRepository.delete_by_id(id)
        logger.info(f"Dedication type with id {id} deleted successfully")
        return result
