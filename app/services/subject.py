import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import SubjectRepository
from app.repositories import AuthorityRepository

logger = logging.getLogger(__name__)


class SubjectService:
    @staticmethod
    @transaction.atomic
    def create(subject_data: dict) -> Any:
        logger.info(f"Creating subject: {subject_data.get('name')}")

        code = subject_data.get("code")
        if code and SubjectRepository.exists_by_code(code):
            logger.error(f"Subject code {code} already exists")
            raise ValueError(f"Subject code '{code}' is already taken")

        created_subject = SubjectRepository.create(subject_data)
        logger.info(f"Subject created successfully with id: {created_subject.id}")
        return created_subject

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding subject with id: {id}")
        subject = SubjectRepository.find_by_id(id)
        if not subject:
            logger.warning(f"Subject with id {id} not found")
        return subject

    @staticmethod
    def find_by_code(code: str) -> Optional[Any]:
        logger.info(f"Finding subject with code: {code}")
        subject = SubjectRepository.find_by_code(code)
        if not subject:
            logger.warning(f"Subject with code '{code}' not found")
        return subject

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all subjects")
        subjects = SubjectRepository.find_all()
        logger.info(f"Found {len(subjects)} subjects")
        return subjects

    @staticmethod
    @transaction.atomic
    def update(id: int, subject_data: dict) -> Any:
        logger.info(f"Updating subject with id: {id}")

        existing_subject = SubjectRepository.find_by_id(id)
        if not existing_subject:
            logger.error(f"Subject with id {id} not found for update")
            raise ValueError(f"Subject with id {id} does not exist")

        code = subject_data.get("code")
        if code and code != existing_subject.code:
            if SubjectRepository.exists_by_code(code):
                logger.error(f"Subject code {code} already exists")
                raise ValueError(f"Subject code '{code}' is already taken")

        for key, value in subject_data.items():
            if hasattr(existing_subject, key):
                setattr(existing_subject, key, value)

        updated_subject = SubjectRepository.update(existing_subject)
        logger.info(f"Subject with id {id} updated successfully")
        return updated_subject

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting subject with id: {id}")

        if not SubjectRepository.exists_by_id(id):
            logger.error(f"Subject with id {id} not found for deletion")
            raise ValueError(f"Subject with id {id} does not exist")

        result = SubjectRepository.delete_by_id(id)
        logger.info(f"Subject with id {id} deleted successfully")
        return result

    @staticmethod
    @transaction.atomic
    def associate_authority(subject_id: int, authority_id: int) -> None:
        logger.info(f"Associating authority {authority_id} with subject {subject_id}")

        subject = SubjectRepository.find_by_id(subject_id)
        if not subject:
            logger.error(f"Subject with id {subject_id} not found")
            raise ValueError(f"Subject with id {subject_id} does not exist")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        if SubjectRepository.is_authority_associated(subject, authority):
            logger.warning(
                f"Authority {authority_id} is already associated with subject {subject_id}"
            )
            raise ValueError(
                f"Authority {authority_id} is already associated with this subject"
            )

        SubjectRepository.associate_authority(subject, authority)
        logger.info(
            f"Authority {authority_id} associated successfully with subject {subject_id}"
        )

    @staticmethod
    @transaction.atomic
    def disassociate_authority(subject_id: int, authority_id: int) -> None:
        logger.info(
            f"Disassociating authority {authority_id} from subject {subject_id}"
        )

        subject = SubjectRepository.find_by_id(subject_id)
        if not subject:
            logger.error(f"Subject with id {subject_id} not found")
            raise ValueError(f"Subject with id {subject_id} does not exist")

        authority = AuthorityRepository.find_by_id(authority_id)
        if not authority:
            logger.error(f"Authority with id {authority_id} not found")
            raise ValueError(f"Authority with id {authority_id} does not exist")

        if not SubjectRepository.is_authority_associated(subject, authority):
            logger.warning(
                f"Authority {authority_id} is not associated with subject {subject_id}"
            )
            raise ValueError(
                f"Authority {authority_id} is not associated with this subject"
            )

        SubjectRepository.disassociate_authority(subject, authority)
        logger.info(
            f"Authority {authority_id} disassociated successfully from subject {subject_id}"
        )
