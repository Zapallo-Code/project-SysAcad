import logging
from django.db import transaction
from app.models.area import Area
from app.repositories.area import AreaRepository

logger = logging.getLogger(__name__)


class AreaService:
    @staticmethod
    @transaction.atomic
    def create(area):
        logger.info(f"Creating area: {area.name}")
        AreaRepository.create(area)
        logger.info(f"Area created successfully with id: {area.id}")

    @staticmethod
    def find_by_id(id: int) -> Area:
        logger.info(f"Finding area with id: {id}")
        area = AreaRepository.find_by_id(id)
        if not area:
            logger.warning(f"Area with id {id} not found")
        return area

    @staticmethod
    def find_all() -> list[Area]:
        logger.info("Finding all areas")
        return AreaRepository.find_all()

    @staticmethod
    @transaction.atomic
    def update(id: int, area: Area) -> Area:
        logger.info(f"Updating area with id: {id}")
        existing_area = AreaRepository.find_by_id(id)
        if not existing_area:
            logger.error(f"Area with id {id} not found for update")
            return None
        existing_area.name = area.name
        updated_area = AreaRepository.update(existing_area)
        logger.info(f"Area with id {id} updated successfully")
        return updated_area

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting area with id: {id}")
        result = AreaRepository.delete_by_id(id)
        if result:
            logger.info(f"Area with id {id} deleted successfully")
        else:
            logger.warning(f"Area with id {id} not found for deletion")
        return result
