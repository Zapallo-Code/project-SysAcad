import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import DocumentTypeRepository

logger = logging.getLogger(__name__)


class DocumentTypeService:

    @staticmethod
    @transaction.atomic
    def create(document_type_data: dict) -> Any:
        logger.info("Creating document type")

        created_document_type = DocumentTypeRepository.create(document_type_data)
        logger.info(f"Document type created successfully with id: {created_document_type.id}")
        return created_document_type

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding document type with id: {id}")
        document_type = DocumentTypeRepository.find_by_id(id)
        if not document_type:
            logger.warning(f"Document type with id {id} not found")
        return document_type

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all document types")
        document_types = DocumentTypeRepository.find_all()
        logger.info(f"Found {len(document_types)} document types")
        return document_types

    @staticmethod
    @transaction.atomic
    def update(id: int, document_type_data: dict) -> Any:
        logger.info(f"Updating document type with id: {id}")

        existing_document_type = DocumentTypeRepository.find_by_id(id)
        if not existing_document_type:
            logger.error(f"Document type with id {id} not found for update")
            raise ValueError(f"Document type with id {id} does not exist")

        for key, value in document_type_data.items():
            if hasattr(existing_document_type, key):
                setattr(existing_document_type, key, value)

        updated_document_type = DocumentTypeRepository.update(existing_document_type)
        logger.info(f"Document type with id {id} updated successfully")
        return updated_document_type

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting document type with id: {id}")

        if not DocumentTypeRepository.exists_by_id(id):
            logger.error(f"Document type with id {id} not found for deletion")
            raise ValueError(f"Document type with id {id} does not exist")

        result = DocumentTypeRepository.delete_by_id(id)
        logger.info(f"Document type with id {id} deleted successfully")
        return result
