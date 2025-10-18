import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import PositionRepository
from app.repositories import PositionCategoryRepository
from app.repositories import DedicationTypeRepository

logger = logging.getLogger(__name__)


class PositionService:

    @staticmethod
    @transaction.atomic
    def create(position_data: dict) -> Any:
        logger.info(f"Creating position: {position_data.get('name')}")

        if PositionRepository.exists_by_name(position_data.get("name")):
            logger.error(f"Position name {position_data.get('name')} already exists")
            raise ValueError(
                f"Position name '{position_data.get('name')}' is already taken"
            )

        position_category_id = position_data.get("position_category_id")
        if position_category_id and not PositionCategoryRepository.exists_by_id(
            position_category_id
        ):
            logger.error(f"Position category with id {position_category_id} not found")
            raise ValueError(
                f"Position category with id {position_category_id} does not exist"
            )

        dedication_type_id = position_data.get("dedication_type_id")
        if dedication_type_id and not DedicationTypeRepository.exists_by_id(
            dedication_type_id
        ):
            logger.error(f"Dedication type with id {dedication_type_id} not found")
            raise ValueError(
                f"Dedication type with id {dedication_type_id} does not exist"
            )

        created_position = PositionRepository.create(position_data)
        logger.info(f"Position created successfully with id: {created_position.id}")
        return created_position

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding position with id: {id}")
        position = PositionRepository.find_by_id(id)
        if not position:
            logger.warning(f"Position with id {id} not found")
        return position

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding position with name: {name}")
        position = PositionRepository.find_by_name(name)
        if not position:
            logger.warning(f"Position with name '{name}' not found")
        return position

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all positions")
        positions = PositionRepository.find_all()
        logger.info(f"Found {len(positions)} positions")
        return positions

    @staticmethod
    def find_by_category(position_category_id: int) -> List[Any]:
        logger.info(f"Finding positions by category id: {position_category_id}")

        if not PositionCategoryRepository.exists_by_id(position_category_id):
            logger.error(f"Position category with id {position_category_id} not found")
            raise ValueError(
                f"Position category with id {position_category_id} does not exist"
            )

        positions = PositionRepository.find_by_category(position_category_id)
        logger.info(
            f"Found {len(positions)} positions for category {position_category_id}"
        )
        return positions

    @staticmethod
    @transaction.atomic
    def update(id: int, position_data: dict) -> Any:
        logger.info(f"Updating position with id: {id}")

        existing_position = PositionRepository.find_by_id(id)
        if not existing_position:
            logger.error(f"Position with id {id} not found for update")
            raise ValueError(f"Position with id {id} does not exist")

        name = position_data.get("name")
        if name and name != existing_position.name:
            if PositionRepository.exists_by_name(name):
                logger.error(f"Position name {name} already exists")
                raise ValueError(f"Position name '{name}' is already taken")

        position_category_id = position_data.get("position_category_id")
        if position_category_id and not PositionCategoryRepository.exists_by_id(
            position_category_id
        ):
            logger.error(f"Position category with id {position_category_id} not found")
            raise ValueError(
                f"Position category with id {position_category_id} does not exist"
            )

        dedication_type_id = position_data.get("dedication_type_id")
        if dedication_type_id and not DedicationTypeRepository.exists_by_id(
            dedication_type_id
        ):
            logger.error(f"Dedication type with id {dedication_type_id} not found")
            raise ValueError(
                f"Dedication type with id {dedication_type_id} does not exist"
            )

        for key, value in position_data.items():
            if hasattr(existing_position, key):
                setattr(existing_position, key, value)

        updated_position = PositionRepository.update(existing_position)
        logger.info(f"Position with id {id} updated successfully")
        return updated_position

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting position with id: {id}")

        if not PositionRepository.exists_by_id(id):
            logger.error(f"Position with id {id} not found for deletion")
            raise ValueError(f"Position with id {id} does not exist")

        result = PositionRepository.delete_by_id(id)
        logger.info(f"Position with id {id} deleted successfully")
        return result
