from django.core.exceptions import ObjectDoesNotExist
from app.models.subject import Subject
from app.models.authority import Authority


class SubjectRepository:
    @staticmethod
    def create(subject):
        subject.save()
        return subject

    @staticmethod
    def find_by_id(id: int):
        try:
            return Subject.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all():
        return Subject.objects.all()

    @staticmethod
    def update(subject) -> Subject:
        subject.save()
        return subject

    @staticmethod
    def delete_by_id(id: int) -> bool:
        subject = SubjectRepository.find_by_id(id)
        if not subject:
            return False
        subject.delete()
        return True

    @staticmethod
    def associate_authority(subject: Subject, authority: Authority):
        # En Django, accedemos a la relación inversa desde Authority
        authority.subjects.add(subject)

    @staticmethod
    def disassociate_authority(subject: Subject, authority: Authority):
        # En Django, accedemos a la relación inversa desde Authority
        authority.subjects.remove(subject)
    
    @staticmethod
    def find_by_code(code: str):
        try:
            return Subject.objects.get(code=code)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_by_name(name: str):
        return Subject.objects.filter(name__icontains=name)
    
    @staticmethod
    def find_with_relations(id: int):
        try:
            return Subject.objects.prefetch_related('authorities').get(id=id)
        except ObjectDoesNotExist:
            return None

