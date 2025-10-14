from app.models.faculty import Faculty
from app.repositories.faculty_repository import FacultyRepository
from app.repositories.authority_repository import AuthorityRepository

class FacultyService:
    
    @staticmethod
    def create(faculty: Faculty):
        FacultyRepository.create(faculty)
    
    @staticmethod
    def find_by_id(id: int) -> Faculty:
        return FacultyRepository.find_by_id(id)
    
    @staticmethod
    def find_all() -> list[Faculty]:
        return FacultyRepository.find_all()
    
    @staticmethod
    def update(id: int, faculty: Faculty) -> Faculty:
        existing_faculty = FacultyRepository.find_by_id(id)
        if not existing_faculty:
            return None
        existing_faculty.name = faculty.name
        existing_faculty.abbreviation = faculty.abbreviation
        existing_faculty.directory = faculty.directory
        existing_faculty.acronym = faculty.acronym
        existing_faculty.postal_code = faculty.postal_code
        existing_faculty.city = faculty.city
        existing_faculty.address = faculty.address
        existing_faculty.phone = faculty.phone
        existing_faculty.contact_name = faculty.contact_name
        existing_faculty.email = faculty.email
        existing_faculty.university = faculty.university
        return FacultyRepository.update(existing_faculty)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return FacultyRepository.delete_by_id(id)
    
    @staticmethod
    def associate_authority(faculty_id: int, authority_id: int):
        faculty = FacultyRepository.find_by_id(faculty_id)
        authority = AuthorityRepository.find_by_id(authority_id)
        if not faculty or not authority:
            raise ValueError("Faculty or authority not found")
        FacultyRepository.associate_authority(faculty, authority)

    @staticmethod
    def disassociate_authority(faculty_id: int, authority_id: int):
        faculty = FacultyRepository.find_by_id(faculty_id)
        authority = AuthorityRepository.find_by_id(authority_id)
        if not faculty or not authority:
            raise ValueError("Faculty or authority not found")
        FacultyRepository.disassociate_authority(faculty, authority)

