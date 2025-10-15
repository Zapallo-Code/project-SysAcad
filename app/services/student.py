import datetime
import logging
from io import BytesIO
from django.db import transaction
from app.models.student import Student
from app.repositories.student import StudentRepository
from app.services.certificate import get_document_type

logger = logging.getLogger(__name__)


class StudentService:

    @staticmethod
    @transaction.atomic
    def create(student):
        logger.info(f"Creating student: {student.first_name} {student.last_name}")
        StudentRepository.create(student)
        logger.info(f"Student created successfully with id: {student.id}")

    @staticmethod
    def find_by_id(id: int) -> Student:
        logger.info(f"Finding student with id: {id}")
        student = StudentRepository.find_by_id(id)
        if not student:
            logger.warning(f"Student with id {id} not found")
        return student

    @staticmethod
    def find_all() -> list[Student]:
        logger.info("Finding all students")
        return StudentRepository.find_all()

    @staticmethod
    @transaction.atomic
    def update(id: int, student: Student) -> Student:
        logger.info(f"Updating student with id: {id}")
        existing_student = StudentRepository.find_by_id(id)
        if not existing_student:
            logger.warning(f"Student with id {id} not found for update")
            return None
        existing_student.first_name = student.first_name
        existing_student.last_name = student.last_name
        existing_student.document_number = student.document_number
        existing_student.document_type = student.document_type
        existing_student.birth_date = student.birth_date
        existing_student.gender = student.gender
        existing_student.student_number = student.student_number
        existing_student.enrollment_date = student.enrollment_date
        existing_student.specialty = student.specialty
        updated_student = StudentRepository.update(existing_student)
        logger.info(f"Student with id {id} updated successfully")
        return updated_student

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting student with id: {id}")
        result = StudentRepository.delete_by_id(id)
        if result:
            logger.info(f"Student with id {id} deleted successfully")
        else:
            logger.warning(f"Student with id {id} not found for deletion")
        return result

    @staticmethod
    def generar_certificado_alumno_regular(id: int, tipo: str) -> BytesIO:
        student = StudentRepository.find_by_id(id)
        if not student:
            raise ValueError(f"Student with id {id} not found")

        context = StudentService._get_student_data(student)
        documento = get_document_type(tipo)
        if not documento:
            raise ValueError(f"Document type '{tipo}' is not supported")

        return documento.generar(
            folder='certificado',
            template='certificado_pdf',
            context=context
        )

    @staticmethod
    def _get_current_date():
        current_date = datetime.datetime.now()
        date_str = current_date.strftime('%d de %B de %Y')
        return date_str

    @staticmethod
    def _get_student_data(student: Student) -> dict:
        specialty = student.specialty
        faculty = specialty.faculty
        university = faculty.university
        return {
            "student": student,
            "specialty": specialty,
            "faculty": faculty,
            "university": university,
            "date": StudentService._get_current_date()
        }
