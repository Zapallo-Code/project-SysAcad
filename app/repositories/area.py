from django.core.exceptions import ObjectDoesNotExist
from app.models.area import Area


class AreaRepository:
    @staticmethod
    def create(area):
        area.save()
        return area

    @staticmethod
    def find_by_id(id: int):
        try:
            return Area.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Area.objects.all()

    @staticmethod
    def update(area) -> Area:
        area.save()
        return area

    @staticmethod
    def delete_by_id(id: int) -> bool:
        area = AreaRepository.find_by_id(id)
        if not area:
            return False
        area.delete()
        return True

    @staticmethod
    def find_by_name(name: str):
        return Area.objects.filter(name__icontains=name)
