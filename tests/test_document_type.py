from django.test import TestCase
from app.models.document_type import DocumentType
from app.services import DocumentTypeService
from tests.fixtures import new_document_type

class DocumentTypeTestCase(TestCase):

    def test_crear(self):
        document_type = new_document_type()
        self.assertIsNotNone(document_type)
        self.assertIsNotNone(document_type.id)
        self.assertGreaterEqual(document_type.id, 1)
        self.assertEqual(document_type.dni, 46291002)

    def test_find_by_id(self):
        document_type = new_document_type()
        r = DocumentTypeService.find_by_id(document_type.id)
        self.assertIsNotNone(r)
        self.assertEqual(r.dni, 46291002)
        self.assertEqual(r.civic_card, "nacional")

    def test_buscar_todos(self):
        document_type1 = new_document_type()
        document_type2 = new_document_type(48291002, "23456789", "98765432", "CD123456")
        documentos = DocumentTypeService.find_all()
        self.assertIsNotNone(documentos)
        self.assertEqual(len(documentos), 2)

    def test_actualizar(self):
        document_type = new_document_type()
        document_type.dni = 89291002
        document_type_actualizado = DocumentTypeService.update(document_type.id, document_type)
        self.assertEqual(document_type_actualizado.dni, 89291002)
    
    def test_borrar(self):
        document_type = new_document_type()
        borrado = DocumentTypeService.delete_by_id(document_type.id)
        self.assertTrue(borrado)
        resultado = DocumentTypeService.find_by_id(document_type.id)
        self.assertIsNone(resultado)
