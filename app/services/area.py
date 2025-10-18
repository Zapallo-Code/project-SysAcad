import logging
from typing import Any, Optional, List
from django.db import transaction
from app.repositories import AreaRepository

logger = logging.getLogger(__name__)


class AreaService:

    @staticmethod
    @transaction.atomic
    def create(area_data: dict) -> Any:
        logger.info(f"Creating area: {area_data.get('name')}")

        if AreaRepository.exists_by_name(area_data.get("name")):
            logger.error(f"Area name {area_data.get('name')} already exists")
            raise ValueError(f"Area name '{area_data.get('name')}' is already taken")

        created_area = AreaRepository.create(area_data)
        logger.info(f"Area created successfully with id: {created_area.id}")
        return created_area

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding area with id: {id}")
        area = AreaRepository.find_by_id(id)
        if not area:
            logger.warning(f"Area with id {id} not found")
        return area

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding area with name: {name}")
        area = AreaRepository.find_by_name(name)
        if not area:
            logger.warning(f"Area with name '{name}' not found")
        return area

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all areas")
        areas = AreaRepository.find_all()
        logger.info(f"Found {len(areas)} areas")
        return areas

    @staticmethod
    @transaction.atomic
    def update(id: int, area_data: dict) -> Any:
        logger.info(f"Updating area with id: {id}")

        existing_area = AreaRepository.find_by_id(id)
        if not existing_area:
            logger.error(f"Area with id {id} not found for update")
            raise ValueError(f"Area with id {id} does not exist")

        name = area_data.get("name")
        if name and name != existing_area.name:
            if AreaRepository.exists_by_name(name):
                logger.error(f"Area name {name} already exists")
                raise ValueError(f"Area name '{name}' is already taken")

        for key, value in area_data.items():
            if hasattr(existing_area, key):
                setattr(existing_area, key, value)

        updated_area = AreaRepository.update(existing_area)
        logger.info(f"Area with id {id} updated successfully")
        return updated_area

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting area with id: {id}")

        if not AreaRepository.exists_by_id(id):
            logger.error(f"Area with id {id} not found for deletion")
            raise ValueError(f"Area with id {id} does not exist")

        result = AreaRepository.delete_by_id(id)
        logger.info(f"Area with id {id} deleted successfully")
        return result
