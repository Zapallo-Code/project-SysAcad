from app.models.area import Area
from app.repositories.area import AreaRepository


class AreaService:
    @staticmethod
    def create(area):
        AreaRepository.create(area)

    @staticmethod
    def find_by_id(id: int) -> Area:
        return AreaRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Area]:
        return AreaRepository.find_all()

    @staticmethod
    def update(id: int, area: Area) -> Area:
        existing_area = AreaRepository.find_by_id(id)
        if not existing_area:
            raise ValueError(f"Area with id {id} not found")
        existing_area.name = area.name
        return AreaRepository.update(existing_area)

    @staticmethod
    def delete_by_id(id: int) -> bool:
        return AreaRepository.delete_by_id(id)
