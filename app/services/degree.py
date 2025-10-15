import logging
from django.db import transaction
from app.models.degree import Degree
from app.repositories.degree import DegreeRepository

logger = logging.getLogger(__name__)


class DegreeService:

    @staticmethod
    @transaction.atomic
    def create(grado: Degree):
        logger.info(f"Creating degree: {grado.name}")
        DegreeRepository.create(grado)
        logger.info(f"Degree created successfully with id: {grado.id}")

    @staticmethod
    def find_by_id(id: int) -> Degree:
        logger.info(f"Finding degree with id: {id}")
        degree = DegreeRepository.find_by_id(id)
        if not degree:
            logger.warning(f"Degree with id {id} not found")
        return degree

    @staticmethod
    def find_all() -> list[Degree]:
        logger.info("Finding all degrees")
        return DegreeRepository.find_all()

    @staticmethod
    @transaction.atomic
    def update(id: int, grado: Degree) -> Degree:
        logger.info(f"Updating degree with id: {id}")
        existing_degree = DegreeRepository.find_by_id(id)
        if not existing_degree:
            logger.warning(f"Degree with id {id} not found for update")
            return None
        existing_degree.name = grado.name
        existing_degree.description = grado.description
        updated_degree = DegreeRepository.update(existing_degree)
        logger.info(f"Degree with id {id} updated successfully")
        return updated_degree

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting degree with id: {id}")
        result = DegreeRepository.delete_by_id(id)
        if result:
            logger.info(f"Degree with id {id} deleted successfully")
        else:
            logger.warning(f"Degree with id {id} not found for deletion")
        return result
