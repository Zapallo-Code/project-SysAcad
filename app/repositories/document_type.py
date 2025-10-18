from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist
from app.models import DocumentType


class DocumentTypeRepository:
    @staticmethod
    def create(document_type_data: Dict[str, Any]) -> DocumentType:
        document_type = DocumentType(**document_type_data)
        document_type.full_clean()
        document_type.save()
        return document_type

    @staticmethod
    def find_by_id(id: int) -> Optional[DocumentType]:
        try:
            return DocumentType.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_all() -> List[DocumentType]:
        return list(DocumentType.objects.all())

    @staticmethod
    def find_by_name(name: str) -> Optional[DocumentType]:
        """Find a document type by its name."""
        try:
            return DocumentType.objects.get(name=name)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_dni(dni: int) -> Optional[DocumentType]:
        try:
            return DocumentType.objects.get(dni=dni)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_passport(passport: str) -> Optional[DocumentType]:
        try:
            return DocumentType.objects.get(passport=passport)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def update(document_type: DocumentType) -> DocumentType:
        document_type.full_clean()
        document_type.save()
        return document_type

    @staticmethod
    def delete_by_id(id: int) -> bool:
        document_type = DocumentTypeRepository.find_by_id(id)
        if not document_type:
            return False
        document_type.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return DocumentType.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_dni(dni: int) -> bool:
        return DocumentType.objects.filter(dni=dni).exists()

    @staticmethod
    def count() -> int:
        return DocumentType.objects.count()
