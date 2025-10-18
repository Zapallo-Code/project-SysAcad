import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import PositionCategoryRepository

logger = logging.getLogger(__name__)


class PositionCategoryService:

    @staticmethod
    @transaction.atomic
    def create(position_category_data: dict) -> Any:
        logger.info(f"Creating position category: {position_category_data.get('name')}")

        if PositionCategoryRepository.exists_by_name(
            position_category_data.get("name")
        ):
            logger.error(
                f"Position category name {position_category_data.get('name')} already exists"
            )
            raise ValueError(
                f"Position category name '{position_category_data.get('name')}' is already taken"
            )

        created_position_category = PositionCategoryRepository.create(
            position_category_data
        )
        logger.info(
            f"Position category created successfully with id: {created_position_category.id}"
        )
        return created_position_category

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding position category with id: {id}")
        position_category = PositionCategoryRepository.find_by_id(id)
        if not position_category:
            logger.warning(f"Position category with id {id} not found")
        return position_category

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding position category with name: {name}")
        position_category = PositionCategoryRepository.find_by_name(name)
        if not position_category:
            logger.warning(f"Position category with name '{name}' not found")
        return position_category

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all position categories")
        position_categories = PositionCategoryRepository.find_all()
        logger.info(f"Found {len(position_categories)} position categories")
        return position_categories

    @staticmethod
    @transaction.atomic
    def update(id: int, position_category_data: dict) -> Any:
        logger.info(f"Updating position category with id: {id}")

        existing_position_category = PositionCategoryRepository.find_by_id(id)
        if not existing_position_category:
            logger.error(f"Position category with id {id} not found for update")
            raise ValueError(f"Position category with id {id} does not exist")

        name = position_category_data.get("name")
        if name and name != existing_position_category.name:
            if PositionCategoryRepository.exists_by_name(name):
                logger.error(f"Position category name {name} already exists")
                raise ValueError(f"Position category name '{name}' is already taken")

        for key, value in position_category_data.items():
            if hasattr(existing_position_category, key):
                setattr(existing_position_category, key, value)

        updated_position_category = PositionCategoryRepository.update(
            existing_position_category
        )
        logger.info(f"Position category with id {id} updated successfully")
        return updated_position_category

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting position category with id: {id}")

        if not PositionCategoryRepository.exists_by_id(id):
            logger.error(f"Position category with id {id} not found for deletion")
            raise ValueError(f"Position category with id {id} does not exist")

        result = PositionCategoryRepository.delete_by_id(id)
        logger.info(f"Position category with id {id} deleted successfully")
        return result
