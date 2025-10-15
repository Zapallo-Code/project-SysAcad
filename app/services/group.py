from app.models.group import Group
from app.repositories.group import GroupRepository


class GroupService:
    @staticmethod
    def create(group):
        GroupRepository.create(group)

    @staticmethod
    def find_by_id(id: int) -> Group:
        return GroupRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Group]:
        return GroupRepository.find_all()

    @staticmethod
    def update(id: int, group: Group) -> Group:
        existing_group = GroupRepository.find_by_id(id)
        if not existing_group:
            return None
        existing_group.name = group.name
        return GroupRepository.update(existing_group)

    @staticmethod
    def delete_by_id(id: int) -> bool:
        return GroupRepository.delete_by_id(id)
