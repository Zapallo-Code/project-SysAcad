import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import DegreeRepository

logger = logging.getLogger(__name__)


class DegreeService:

    @staticmethod
    @transaction.atomic
    def create(degree_data: dict) -> Any:
        logger.info(f"Creating degree: {degree_data.get('name')}")

        if DegreeRepository.exists_by_name(degree_data.get('name')):
            logger.error(f"Degree name {degree_data.get('name')} already exists")
            raise ValueError(f"Degree name '{degree_data.get('name')}' is already taken")

        created_degree = DegreeRepository.create(degree_data)
        logger.info(f"Degree created successfully with id: {created_degree.id}")
        return created_degree

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding degree with id: {id}")
        degree = DegreeRepository.find_by_id(id)
        if not degree:
            logger.warning(f"Degree with id {id} not found")
        return degree

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding degree with name: {name}")
        degree = DegreeRepository.find_by_name(name)
        if not degree:
            logger.warning(f"Degree with name '{name}' not found")
        return degree

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all degrees")
        degrees = DegreeRepository.find_all()
        logger.info(f"Found {len(degrees)} degrees")
        return degrees

    @staticmethod
    @transaction.atomic
    def update(id: int, degree_data: dict) -> Any:
        logger.info(f"Updating degree with id: {id}")

        existing_degree = DegreeRepository.find_by_id(id)
        if not existing_degree:
            logger.error(f"Degree with id {id} not found for update")
            raise ValueError(f"Degree with id {id} does not exist")

        name = degree_data.get('name')
        if name and name != existing_degree.name:
            if DegreeRepository.exists_by_name(name):
                logger.error(f"Degree name {name} already exists")
                raise ValueError(f"Degree name '{name}' is already taken")

        for key, value in degree_data.items():
            if hasattr(existing_degree, key):
                setattr(existing_degree, key, value)

        updated_degree = DegreeRepository.update(existing_degree)
        logger.info(f"Degree with id {id} updated successfully")
        return updated_degree

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting degree with id: {id}")

        if not DegreeRepository.exists_by_id(id):
            logger.error(f"Degree with id {id} not found for deletion")
            raise ValueError(f"Degree with id {id} does not exist")

        result = DegreeRepository.delete_by_id(id)
        logger.info(f"Degree with id {id} deleted successfully")
        return result
