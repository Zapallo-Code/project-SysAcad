from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import Group


class GroupRepository:
    @staticmethod
    def create(group_data: Dict[str, Any]) -> Group:
        group = Group(**group_data)
        group.full_clean()
        group.save()
        return group

    @staticmethod
    def find_by_id(id: int) -> Optional[Group]:
        try:
            return Group.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_name(name: str) -> Optional[Group]:
        try:
            return Group.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def search_by_name(name: str) -> List[Group]:
        return list(Group.objects.filter(name__icontains=name))

    @staticmethod
    def find_all() -> List[Group]:
        return list(Group.objects.all())

    @staticmethod
    def find_by_subject(subject_id: int) -> List[Group]:
        """Find all groups for a specific subject."""
        return list(Group.objects.filter(subject_id=subject_id).select_related("subject"))

    @staticmethod
    def find_by_code(code: str) -> Optional[Group]:
        """Find a group by its code."""
        try:
            return Group.objects.get(code=code)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(group: Group) -> Group:
        group.full_clean()
        group.save()
        return group

    @staticmethod
    def delete(id: int) -> bool:
        """Delete a group by ID."""
        group = GroupRepository.find_by_id(id)
        if not group:
            return False
        group.delete()
        return True

    @staticmethod
    def delete_by_id(id: int) -> bool:
        group = GroupRepository.find_by_id(id)
        if not group:
            return False
        group.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Group.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_name(name: str) -> bool:
        return Group.objects.filter(name=name).exists()

    @staticmethod
    def exists_by_code(code: str) -> bool:
        """Check if a group exists by code."""
        return Group.objects.filter(code=code).exists()

    @staticmethod
    def count() -> int:
        return Group.objects.count()
