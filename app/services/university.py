import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories.university import UniversityRepository

logger = logging.getLogger(__name__)


class UniversityService:

    @staticmethod
    @transaction.atomic
    def create(university_data: dict) -> Any:
        logger.info(f"Creating university: {university_data.get('name')}")

        if UniversityRepository.exists_by_name(university_data.get('name')):
            logger.error(f"University name {university_data.get('name')} already exists")
            raise ValueError(f"University name '{university_data.get('name')}' is already taken")

        acronym = university_data.get('acronym')
        if acronym and UniversityRepository.exists_by_acronym(acronym):
            logger.error(f"University acronym {acronym} already exists")
            raise ValueError(f"University acronym '{acronym}' is already taken")

        created_university = UniversityRepository.create(university_data)
        logger.info(f"University created successfully with id: {created_university.id}")
        return created_university

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding university with id: {id}")
        university = UniversityRepository.find_by_id(id)
        if not university:
            logger.warning(f"University with id {id} not found")
        return university

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding university with name: {name}")
        university = UniversityRepository.find_by_name(name)
        if not university:
            logger.warning(f"University with name '{name}' not found")
        return university

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all universities")
        universities = UniversityRepository.find_all()
        logger.info(f"Found {len(universities)} universities")
        return universities

    @staticmethod
    @transaction.atomic
    def update(id: int, university_data: dict) -> Any:
        logger.info(f"Updating university with id: {id}")

        existing_university = UniversityRepository.find_by_id(id)
        if not existing_university:
            logger.error(f"University with id {id} not found for update")
            raise ValueError(f"University with id {id} does not exist")

        name = university_data.get('name')
        if name and name != existing_university.name:
            if UniversityRepository.exists_by_name(name):
                logger.error(f"University name {name} already exists")
                raise ValueError(f"University name '{name}' is already taken")

        acronym = university_data.get('acronym')
        if acronym and acronym != existing_university.acronym:
            if UniversityRepository.exists_by_acronym(acronym):
                logger.error(f"University acronym {acronym} already exists")
                raise ValueError(f"University acronym '{acronym}' is already taken")

        for key, value in university_data.items():
            if hasattr(existing_university, key):
                setattr(existing_university, key, value)

        updated_university = UniversityRepository.update(existing_university)
        logger.info(f"University with id {id} updated successfully")
        return updated_university

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting university with id: {id}")

        if not UniversityRepository.exists_by_id(id):
            logger.error(f"University with id {id} not found for deletion")
            raise ValueError(f"University with id {id} does not exist")

        result = UniversityRepository.delete_by_id(id)
        logger.info(f"University with id {id} deleted successfully")
        return result
