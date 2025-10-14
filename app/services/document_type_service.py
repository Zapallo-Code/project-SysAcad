from app.models.document_type import DocumentType
from app.repositories.document_type_repository import DocumentTypeRepository

class DocumentTypeService:

    @staticmethod
    def create(document_type):
        DocumentTypeRepository.create(document_type)

    @staticmethod
    def find_by_id(id: int) -> DocumentType:
        return DocumentTypeRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[DocumentType]:
        return DocumentTypeRepository.find_all()
    
    @staticmethod
    def update(id: int, document_type: DocumentType) -> DocumentType:
        document_type_existente = DocumentTypeRepository.find_by_id(id)
        if not document_type_existente:
            return None
        document_type_existente.dni = document_type.dni
        document_type_existente.civic_card = document_type.civic_card
        document_type_existente.enrollment_card = document_type.enrollment_card
        document_type_existente.passport = document_type.passport
        return DocumentTypeRepository.update(document_type_existente)
    
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return DocumentTypeRepository.delete_by_id(id)

