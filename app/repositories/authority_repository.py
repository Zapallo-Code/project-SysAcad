from django.core.exceptions import ObjectDoesNotExist
from app.models.authority import Authority
from app.models.subject import Subject
from app.models.faculty import Faculty


class AuthorityRepository:
    @staticmethod
    def create(authority):
        authority.save()
        return authority

    @staticmethod
    def find_by_id(id: int):
        try:
            return Authority.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Authority.objects.all()

    @staticmethod
    def update(authority) -> Authority:
        authority.save()
        return authority
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        authority = AuthorityRepository.find_by_id(id)
        if not authority:
            return False
        authority.delete()
        return True

    @staticmethod
    def associate_subject(authority: Authority, subject: Subject):
        authority.associate_subject(subject)

    @staticmethod
    def disassociate_subject(authority: Authority, subject: Subject):
        authority.disassociate_subject(subject)

    @staticmethod
    def associate_faculty(authority: Authority, faculty: Faculty):
        authority.associate_faculty(faculty)

    @staticmethod
    def disassociate_faculty(authority: Authority, faculty: Faculty):
        authority.disassociate_faculty(faculty)
    
    @staticmethod
    def find_by_position(position_id: int):
        return Authority.objects.filter(position_id=position_id)
    
    @staticmethod
    def find_with_relations(id: int):
        try:
            return Authority.objects.select_related('position').prefetch_related(
                'subjects', 'faculties'
            ).get(id=id)
        except ObjectDoesNotExist:
            return None

