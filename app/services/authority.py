import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import AuthorityRepository
from app.repositories import SubjectRepository
from app.repositories import FacultyRepository
from app.repositories import PositionRepository

logger = logging.getLogger(__name__)


class AuthorityService:

    @staticmethod
    @transaction.atomic
    def create(authority_data: dict) -> Any:
        logger.info(f"Creating authority: {authority_data.get('first_name')} {authority_data.get('last_name')}")

        email = authority_data.get('email')
        if email and AuthorityRepository.exists_by_email(email):
            logger.error(f"Authority email {email} already exists")
            raise ValueError(f"Email '{email}' is already registered")

        position_id = authority_data.get('position_id')
        if position_id and not PositionRepository.exists_by_id(position_id):
            logger.error(f"Position with id {position_id} not found")
            raise ValueError(f"Position with id {position_id} does not exist")

        created_authority = AuthorityRepository.create(authority_data)
        logger.info(f"Authority created successfully with id: {created_authority.id}")
        return created_authority

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding authority with id: {id}")
        authority = AuthorityRepository.find_by_id(id)
        if not authority:
            logger.warning(f"Authority with id {id} not found")
        return authority

    @staticmethod
    def find_by_email(email: str) -> Optional[Any]:
        logger.info(f"Finding authority with email: {email}")
        authority = AuthorityRepository.find_by_email(email)
        if not authority:
            logger.warning(f"Authority with email '{email}' not found")
        return authority

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all authorities")
        authorities = AuthorityRepository.find_all()
        logger.info(f"Found {len(authorities)} authorities")
        return authorities

    @staticmethod
    def find_by_position(position_id: int) -> List[Any]:
        logger.info(f"Finding authorities by position id: {position_id}")

        if not PositionRepository.exists_by_id(position_id):
            logger.error(f"Position with id {position_id} not found")
            raise ValueError(f"Position with id {position_id} does not exist")

        authorities = AuthorityRepository.find_by_position(position_id)
        logger.info(f"Found {len(authorities)} authorities for position {position_id}")
        return authorities

    @staticmethod
    @transaction.atomic
    def update(id: int, authority_data: dict) -> Any:
        logger.info(f"Updating authority with id: {id}")

        existing_authority = AuthorityRepository.find_by_id(id)
        if not existing_authority:
            logger.error(f"Authority with id {id} not found for update")
            raise ValueError(f"Authority with id {id} does not exist")

        email = authority_data.get('email')
        if email and email != existing_authority.email:
            if AuthorityRepository.exists_by_email(email):
                logger.error(f"Authority email {email} already exists")
                raise ValueError(f"Email '{email}' is already registered")

        position_id = authority_data.get('position_id')
        if position_id and not PositionRepository.exists_by_id(position_id):
            logger.error(f"Position with id {position_id} not found")
            raise ValueError(f"Position with id {position_id} does not exist")

        for key, value in authority_data.items():
            if hasattr(existing_authority, key):
                setattr(existing_authority, key, value)

        updated_authority = AuthorityRepository.update(existing_authority)
        logger.info(f"Authority with id {id} updated successfully")
        return updated_authority

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting authority with id: {id}")

        if not AuthorityRepository.exists_by_id(id):
            logger.error(f"Authority with id {id} not found for deletion")
            raise ValueError(f"Authority with id {id} does not exist")

        result = AuthorityRepository.delete_by_id(id)
        logger.info(f"Authority with id {id} deleted successfully")
        return result

    @staticmethod
    @transaction.atomic
    def associate_subject(authority_id: int, subject_id: int) -> None:
        logger.info(f"Associating subject {subject_id} with authority {authority_id}")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        subject = SubjectRepository.find_by_id(subject_id)
        if not subject:
            logger.error(f"Subject with id {subject_id} not found")
            raise ValueError(f"Subject with id {subject_id} does not exist")

        if AuthorityRepository.is_subject_associated(authority, subject):
            logger.warning(f"Subject {subject_id} is already associated with authority {authority_id}")
            raise ValueError(f"Subject {subject_id} is already associated with this authority")

        AuthorityRepository.associate_subject(authority, subject)
        logger.info(f"Subject {subject_id} associated successfully with authority {authority_id}")

    @staticmethod
    @transaction.atomic
    def disassociate_subject(authority_id: int, subject_id: int) -> None:
        logger.info(f"Disassociating subject {subject_id} from authority {authority_id}")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        subject = SubjectRepository.find_by_id(subject_id)
        if not subject:
            logger.error(f"Subject with id {subject_id} not found")
            raise ValueError(f"Subject with id {subject_id} does not exist")

        if not AuthorityRepository.is_subject_associated(authority, subject):
            logger.warning(f"Subject {subject_id} is not associated with authority {authority_id}")
            raise ValueError(f"Subject {subject_id} is not associated with this authority")

        AuthorityRepository.disassociate_subject(authority, subject)
        logger.info(f"Subject {subject_id} disassociated successfully from authority {authority_id}")

    @staticmethod
    @transaction.atomic
    def associate_faculty(authority_id: int, faculty_id: int) -> None:
        logger.info(f"Associating faculty {faculty_id} with authority {authority_id}")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        faculty = FacultyRepository.find_by_id(faculty_id)
        if not faculty:
            logger.error(f"Faculty with id {faculty_id} not found")
            raise ValueError(f"Faculty with id {faculty_id} does not exist")

        if AuthorityRepository.is_faculty_associated(authority, faculty):
            logger.warning(f"Faculty {faculty_id} is already associated with authority {authority_id}")
            raise ValueError(f"Faculty {faculty_id} is already associated with this authority")

        AuthorityRepository.associate_faculty(authority, faculty)
        logger.info(f"Faculty {faculty_id} associated successfully with authority {authority_id}")

    @staticmethod
    @transaction.atomic
    def disassociate_faculty(authority_id: int, faculty_id: int) -> None:
        logger.info(f"Disassociating faculty {faculty_id} from authority {authority_id}")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        faculty = FacultyRepository.find_by_id(faculty_id)
        if not faculty:
            logger.error(f"Faculty with id {faculty_id} not found")
            raise ValueError(f"Faculty with id {faculty_id} does not exist")

        if not AuthorityRepository.is_faculty_associated(authority, faculty):
            logger.warning(f"Faculty {faculty_id} is not associated with authority {authority_id}")
            raise ValueError(f"Faculty {faculty_id} is not associated with this authority")

        AuthorityRepository.disassociate_faculty(authority, faculty)
        logger.info(f"Faculty {faculty_id} disassociated successfully from authority {authority_id}")
