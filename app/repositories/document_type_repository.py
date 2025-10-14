from django.core.exceptions import ObjectDoesNotExist
from app.models.document_type import DocumentType


class DocumentTypeRepository:
    @staticmethod
    def create(document_type):
        document_type.save()
        return document_type

    @staticmethod
    def find_by_id(id: int):
        try:
            return DocumentType.objects.get(id=id)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_all():
        return DocumentType.objects.all()
    
    @staticmethod
    def update(document_type) -> DocumentType:
        document_type.save()
        return document_type
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        document_type = DocumentTypeRepository.find_by_id(id)
        if not document_type:
            return False
        document_type.delete()
        return True

        
