import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import OrientationRepository
from app.repositories import SpecialtyRepository
from app.repositories import PlanRepository
from app.repositories import SubjectRepository

logger = logging.getLogger(__name__)


class OrientationService:

    @staticmethod
    @transaction.atomic
    def create(orientation_data: dict) -> Any:
        logger.info(f"Creating orientation: {orientation_data.get('name')}")

        if OrientationRepository.exists_by_name(orientation_data.get("name")):
            logger.error(
                f"Orientation name {orientation_data.get('name')} already exists"
            )
            raise ValueError(
                f"Orientation name '{orientation_data.get('name')}' is already taken"
            )

        specialty_id = orientation_data.get("specialty_id")
        if specialty_id and not SpecialtyRepository.exists_by_id(specialty_id):
            logger.error(f"Specialty with id {specialty_id} not found")
            raise ValueError(f"Specialty with id {specialty_id} does not exist")

        plan_id = orientation_data.get("plan_id")
        if plan_id and not PlanRepository.exists_by_id(plan_id):
            logger.error(f"Plan with id {plan_id} not found")
            raise ValueError(f"Plan with id {plan_id} does not exist")

        subject_id = orientation_data.get("subject_id")
        if subject_id and not SubjectRepository.exists_by_id(subject_id):
            logger.error(f"Subject with id {subject_id} not found")
            raise ValueError(f"Subject with id {subject_id} does not exist")

        created_orientation = OrientationRepository.create(orientation_data)
        logger.info(
            f"Orientation created successfully with id: {created_orientation.id}"
        )
        return created_orientation

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding orientation with id: {id}")
        orientation = OrientationRepository.find_by_id(id)
        if not orientation:
            logger.warning(f"Orientation with id {id} not found")
        return orientation

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding orientation with name: {name}")
        orientation = OrientationRepository.find_by_name(name)
        if not orientation:
            logger.warning(f"Orientation with name '{name}' not found")
        return orientation

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all orientations")
        orientations = OrientationRepository.find_all()
        logger.info(f"Found {len(orientations)} orientations")
        return orientations

    @staticmethod
    def find_by_specialty(specialty_id: int) -> List[Any]:
        logger.info(f"Finding orientations by specialty id: {specialty_id}")

        if not SpecialtyRepository.exists_by_id(specialty_id):
            logger.error(f"Specialty with id {specialty_id} not found")
            raise ValueError(f"Specialty with id {specialty_id} does not exist")

        orientations = OrientationRepository.find_by_specialty(specialty_id)
        logger.info(
            f"Found {len(orientations)} orientations for specialty {specialty_id}"
        )
        return orientations

    @staticmethod
    @transaction.atomic
    def update(id: int, orientation_data: dict) -> Any:
        logger.info(f"Updating orientation with id: {id}")

        existing_orientation = OrientationRepository.find_by_id(id)
        if not existing_orientation:
            logger.error(f"Orientation with id {id} not found for update")
            raise ValueError(f"Orientation with id {id} does not exist")

        name = orientation_data.get("name")
        if name and name != existing_orientation.name:
            if OrientationRepository.exists_by_name(name):
                logger.error(f"Orientation name {name} already exists")
                raise ValueError(f"Orientation name '{name}' is already taken")

        specialty_id = orientation_data.get("specialty_id")
        if specialty_id and not SpecialtyRepository.exists_by_id(specialty_id):
            logger.error(f"Specialty with id {specialty_id} not found")
            raise ValueError(f"Specialty with id {specialty_id} does not exist")

        plan_id = orientation_data.get("plan_id")
        if plan_id and not PlanRepository.exists_by_id(plan_id):
            logger.error(f"Plan with id {plan_id} not found")
            raise ValueError(f"Plan with id {plan_id} does not exist")

        subject_id = orientation_data.get("subject_id")
        if subject_id and not SubjectRepository.exists_by_id(subject_id):
            logger.error(f"Subject with id {subject_id} not found")
            raise ValueError(f"Subject with id {subject_id} does not exist")

        for key, value in orientation_data.items():
            if hasattr(existing_orientation, key):
                setattr(existing_orientation, key, value)

        updated_orientation = OrientationRepository.update(existing_orientation)
        logger.info(f"Orientation with id {id} updated successfully")
        return updated_orientation

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting orientation with id: {id}")

        if not OrientationRepository.exists_by_id(id):
            logger.error(f"Orientation with id {id} not found for deletion")
            raise ValueError(f"Orientation with id {id} does not exist")

        result = OrientationRepository.delete_by_id(id)
        logger.info(f"Orientation with id {id} deleted successfully")
        return result
