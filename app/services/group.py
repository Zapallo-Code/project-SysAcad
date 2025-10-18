import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import GroupRepository

logger = logging.getLogger(__name__)


class GroupService:
    @staticmethod
    @transaction.atomic
    def create(group_data: dict) -> Any:
        logger.info(f"Creating group: {group_data.get('name')}")

        if GroupRepository.exists_by_name(group_data.get("name")):
            logger.error(f"Group name {group_data.get('name')} already exists")
            raise ValueError(f"Group name '{group_data.get('name')}' is already taken")

        created_group = GroupRepository.create(group_data)
        logger.info(f"Group created successfully with id: {created_group.id}")
        return created_group

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding group with id: {id}")
        group = GroupRepository.find_by_id(id)
        if not group:
            logger.warning(f"Group with id {id} not found")
        return group

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding group with name: {name}")
        group = GroupRepository.find_by_name(name)
        if not group:
            logger.warning(f"Group with name '{name}' not found")
        return group

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all groups")
        groups = GroupRepository.find_all()
        logger.info(f"Found {len(groups)} groups")
        return groups

    @staticmethod
    @transaction.atomic
    def update(id: int, group_data: dict) -> Any:
        logger.info(f"Updating group with id: {id}")

        existing_group = GroupRepository.find_by_id(id)
        if not existing_group:
            logger.error(f"Group with id {id} not found for update")
            raise ValueError(f"Group with id {id} does not exist")

        name = group_data.get("name")
        if name and name != existing_group.name:
            if GroupRepository.exists_by_name(name):
                logger.error(f"Group name {name} already exists")
                raise ValueError(f"Group name '{name}' is already taken")

        for key, value in group_data.items():
            if hasattr(existing_group, key):
                setattr(existing_group, key, value)

        updated_group = GroupRepository.update(existing_group)
        logger.info(f"Group with id {id} updated successfully")
        return updated_group

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting group with id: {id}")

        if not GroupRepository.exists_by_id(id):
            logger.error(f"Group with id {id} not found for deletion")
            raise ValueError(f"Group with id {id} does not exist")

        result = GroupRepository.delete_by_id(id)
        logger.info(f"Group with id {id} deleted successfully")
        return result
