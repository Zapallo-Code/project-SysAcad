from django.core.exceptions import ObjectDoesNotExist
from app.models.faculty import Faculty
from app.models.authority import Authority


class FacultyRepository:
    @staticmethod
    def create(faculty):
        faculty.save()
        return faculty

    @staticmethod
    def find_by_id(id: int):
        try:
            return Faculty.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Faculty.objects.all()

    @staticmethod
    def update(faculty) -> Faculty:
        faculty.save()
        return faculty

    @staticmethod
    def delete_by_id(id: int) -> bool:
        faculty = FacultyRepository.find_by_id(id)
        if not faculty:
            return False
        faculty.delete()
        return True

    @staticmethod
    def associate_authority(faculty: Faculty, authority: Authority):
        # En Django, la relación está definida en Authority
        authority.faculties.add(faculty)

    @staticmethod
    def disassociate_authority(faculty: Faculty, authority: Authority):
        # En Django, la relación está definida en Authority
        authority.faculties.remove(faculty)

    @staticmethod
    def find_by_university(university_id: int):
        return Faculty.objects.filter(university_id=university_id)

    @staticmethod
    def find_by_acronym(acronym: str):
        try:
            return Faculty.objects.get(acronym=acronym)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_with_relations(id: int):
        try:
            return Faculty.objects.select_related('university').prefetch_related(
                'authorities', 'specialties'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None
