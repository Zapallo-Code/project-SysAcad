from django.core.exceptions import ObjectDoesNotExist
from app.models.group import Group


class GroupRepository:
    @staticmethod
    def create(grupo):
        grupo.save()
        return grupo

    @staticmethod
    def find_by_id(id: int):
        try:
            return Group.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_all():
        return Group.objects.all()
    
    @staticmethod
    def update(grupo) -> Group:
        grupo.save()
        return grupo
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        grupo = GroupRepository.find_by_id(id)
        if not grupo:
            return False
        grupo.delete()
        return True
    
    @staticmethod
    def find_by_name(name: str):
        return Group.objects.filter(nombre__icontains=name)

