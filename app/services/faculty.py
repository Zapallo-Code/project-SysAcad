import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import FacultyRepository
from app.repositories import AuthorityRepository
from app.repositories import UniversityRepository

logger = logging.getLogger(__name__)


class FacultyService:

    @staticmethod
    @transaction.atomic
    def create(faculty_data: dict) -> Any:
        logger.info(f"Creating faculty: {faculty_data.get('name')}")

        if FacultyRepository.exists_by_name(faculty_data.get("name")):
            logger.error(f"Faculty name {faculty_data.get('name')} already exists")
            raise ValueError(
                f"Faculty name '{faculty_data.get('name')}' is already taken"
            )

        if faculty_data.get(
            "abbreviation"
        ) and FacultyRepository.exists_by_abbreviation(
            faculty_data.get("abbreviation")
        ):
            logger.error(
                f"Faculty abbreviation {faculty_data.get('abbreviation')} already exists"
            )
            raise ValueError(
                f"Faculty abbreviation '{faculty_data.get('abbreviation')}' is already taken"
            )

        university_id = faculty_data.get("university_id")
        if university_id and not UniversityRepository.exists_by_id(university_id):
            logger.error(f"University with id {university_id} not found")
            raise ValueError(f"University with id {university_id} does not exist")

        created_faculty = FacultyRepository.create(faculty_data)
        logger.info(f"Faculty created successfully with id: {created_faculty.id}")
        return created_faculty

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding faculty with id: {id}")
        faculty = FacultyRepository.find_by_id(id)
        if not faculty:
            logger.warning(f"Faculty with id {id} not found")
        return faculty

    @staticmethod
    def find_by_name(name: str) -> Optional[Any]:
        logger.info(f"Finding faculty with name: {name}")
        faculty = FacultyRepository.find_by_name(name)
        if not faculty:
            logger.warning(f"Faculty with name '{name}' not found")
        return faculty

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all faculties")
        faculties = FacultyRepository.find_all()
        logger.info(f"Found {len(faculties)} faculties")
        return faculties

    @staticmethod
    def find_by_university(university_id: int) -> List[Any]:
        logger.info(f"Finding faculties by university id: {university_id}")

        if not UniversityRepository.exists_by_id(university_id):
            logger.error(f"University with id {university_id} not found")
            raise ValueError(f"University with id {university_id} does not exist")

        faculties = FacultyRepository.find_by_university(university_id)
        logger.info(f"Found {len(faculties)} faculties for university {university_id}")
        return faculties

    @staticmethod
    @transaction.atomic
    def update(id: int, faculty_data: dict) -> Any:
        logger.info(f"Updating faculty with id: {id}")

        existing_faculty = FacultyRepository.find_by_id(id)
        if not existing_faculty:
            logger.error(f"Faculty with id {id} not found for update")
            raise ValueError(f"Faculty with id {id} does not exist")

        name = faculty_data.get("name")
        if name and name != existing_faculty.name:
            if FacultyRepository.exists_by_name(name):
                logger.error(f"Faculty name {name} already exists")
                raise ValueError(f"Faculty name '{name}' is already taken")

        abbreviation = faculty_data.get("abbreviation")
        if abbreviation and abbreviation != existing_faculty.abbreviation:
            if FacultyRepository.exists_by_abbreviation(abbreviation):
                logger.error(f"Faculty abbreviation {abbreviation} already exists")
                raise ValueError(
                    f"Faculty abbreviation '{abbreviation}' is already taken"
                )

        university_id = faculty_data.get("university_id")
        if university_id and not UniversityRepository.exists_by_id(university_id):
            logger.error(f"University with id {university_id} not found")
            raise ValueError(f"University with id {university_id} does not exist")

        for key, value in faculty_data.items():
            if hasattr(existing_faculty, key):
                setattr(existing_faculty, key, value)

        updated_faculty = FacultyRepository.update(existing_faculty)
        logger.info(f"Faculty with id {id} updated successfully")
        return updated_faculty

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting faculty with id: {id}")

        if not FacultyRepository.exists_by_id(id):
            logger.error(f"Faculty with id {id} not found for deletion")
            raise ValueError(f"Faculty with id {id} does not exist")

        result = FacultyRepository.delete_by_id(id)
        logger.info(f"Faculty with id {id} deleted successfully")
        return result

    @staticmethod
    @transaction.atomic
    def associate_authority(faculty_id: int, authority_id: int) -> None:
        logger.info(f"Associating authority {authority_id} with faculty {faculty_id}")

        faculty = FacultyRepository.find_by_id(faculty_id)
        if not faculty:
            logger.error(f"Faculty with id {faculty_id} not found")
            raise ValueError(f"Faculty with id {faculty_id} does not exist")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        if FacultyRepository.is_authority_associated(faculty, authority):
            logger.warning(
                f"Authority {authority_id} is already associated with faculty {faculty_id}"
            )
            raise ValueError(
                f"Authority {authority_id} is already associated with this faculty"
            )

        FacultyRepository.associate_authority(faculty, authority)
        logger.info(
            f"Authority {authority_id} associated successfully with faculty {faculty_id}"
        )

    @staticmethod
    @transaction.atomic
    def disassociate_authority(faculty_id: int, authority_id: int) -> None:
        logger.info(
            f"Disassociating authority {authority_id} from faculty {faculty_id}"
        )

        faculty = FacultyRepository.find_by_id(faculty_id)
        if not faculty:
            logger.error(f"Faculty with id {faculty_id} not found")
            raise ValueError(f"Faculty with id {faculty_id} does not exist")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        if not FacultyRepository.is_authority_associated(faculty, authority):
            logger.warning(
                f"Authority {authority_id} is not associated with faculty {faculty_id}"
            )
            raise ValueError(
                f"Authority {authority_id} is not associated with this faculty"
            )

        FacultyRepository.disassociate_authority(faculty, authority)
        logger.info(
            f"Authority {authority_id} disassociated successfully from faculty {faculty_id}"
        )
