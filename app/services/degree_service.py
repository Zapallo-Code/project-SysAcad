from app.models.degree import Degree
from app.repositories.degree import DegreeRepository

class DegreeService:

    @staticmethod
    def create(grado: Degree):
        DegreeRepository.create(grado)

    @staticmethod
    def find_by_id(id: int) -> Degree:
        return DegreeRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Degree]:
        return DegreeRepository.find_all()

    @staticmethod
    def update(id: int, grado: Degree) -> Degree:
        existing_degree = DegreeRepository.find_by_id(grado.id)
        if not existing_degree:
            return None
        existing_degree.name = grado.name
        existing_degree.description = grado.description
        return DegreeRepository.update(existing_degree)

    @staticmethod
    def delete_by_id(id: int) -> bool:
        return DegreeRepository.delete_by_id(id)

