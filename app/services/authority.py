from app.models.authority import Authority
from app.repositories.authority import AuthorityRepository
from app.repositories.subject import SubjectRepository
from app.repositories.faculty import FacultyRepository


class AuthorityService:
    @staticmethod
    def create(authority):
        AuthorityRepository.create(authority)

    @staticmethod
    def find_by_id(id: int) -> Authority:
        return AuthorityRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Authority]:
        return AuthorityRepository.find_all()

    @staticmethod
    def update(id: int, authority: Authority) -> Authority:
        existing_authority = AuthorityRepository.find_by_id(id)
        if not existing_authority:
            return None
        existing_authority.name = authority.name
        existing_authority.phone = authority.phone
        existing_authority.email = authority.email
        return AuthorityRepository.update(existing_authority)

    @staticmethod
    def delete_by_id(id: int) -> bool:
        return AuthorityRepository.delete_by_id(id)

    @staticmethod
    def associate_subject(authority_id: int, subject_id: int):
        authority = AuthorityRepository.find_by_id(authority_id)
        subject = SubjectRepository.find_by_id(subject_id)
        if not authority or not subject:
            raise ValueError("Subject or authority not found")
        AuthorityRepository.associate_subject(authority, subject)

    @staticmethod
    def disassociate_subject(authority_id: int, subject_id: int):
        authority = AuthorityRepository.find_by_id(authority_id)
        subject = SubjectRepository.find_by_id(subject_id)
        if not authority or not subject:
            raise ValueError("Subject or authority not found")
        AuthorityRepository.disassociate_subject(authority, subject)

    @staticmethod
    def associate_faculty(authority_id: int, faculty_id: int):
        authority = AuthorityRepository.find_by_id(authority_id)
        faculty = FacultyRepository.find_by_id(faculty_id)
        if not authority or not faculty:
            raise ValueError("Faculty or authority not found")
        AuthorityRepository.associate_faculty(authority, faculty)

    @staticmethod
    def disassociate_faculty(authority_id: int, faculty_id: int):
        authority = AuthorityRepository.find_by_id(authority_id)
        faculty = FacultyRepository.find_by_id(faculty_id)
        if not authority or not faculty:
            raise ValueError("Faculty or authority not found")
        AuthorityRepository.disassociate_faculty(authority, faculty)
