from app.models.subject import Subject
from app.repositories.subject import SubjectRepository
from app.repositories.authority import AuthorityRepository


class SubjectService:
    @staticmethod
    def create(subject):
        SubjectRepository.create(subject)

    @staticmethod
    def find_by_id(id: int) -> Subject:
        return SubjectRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Subject]:
        return SubjectRepository.find_all()

    @staticmethod
    def update(id: int, subject: Subject) -> Subject:
        existing_subject = SubjectRepository.find_by_id(id)
        if not existing_subject:
            return None
        existing_subject.name = subject.name
        existing_subject.code = subject.code
        existing_subject.observation = subject.observation
        return SubjectRepository.update(existing_subject)

    @staticmethod
    def delete_by_id(id: int) -> bool:
        return SubjectRepository.delete_by_id(id)

    @staticmethod
    def associate_authority(subject_id: int, authority_id: int):
        subject = SubjectRepository.find_by_id(subject_id)
        authority = AuthorityRepository.find_by_id(authority_id)
        if not subject or not authority:
            raise ValueError("Subject or authority not found")
        SubjectRepository.associate_authority(subject, authority)

    @staticmethod
    def disassociate_authority(subject_id: int, authority_id: int):
        subject = SubjectRepository.find_by_id(subject_id)
        authority = AuthorityRepository.find_by_id(authority_id)
        if not subject or not authority:
            raise ValueError("Subject or authority not found")
        SubjectRepository.disassociate_authority(subject, authority)
