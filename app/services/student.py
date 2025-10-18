import datetime
import logging
from typing import Optional, List, Any
from django.db import transaction
from app.repositories import StudentRepository
from app.repositories import SpecialtyRepository
from app.repositories import DocumentTypeRepository
from app.utils import get_document_generator

logger = logging.getLogger(__name__)


class StudentService:

    @staticmethod
    @transaction.atomic
    def create(student_data: dict) -> Any:
        logger.info(
            f"Creating student: {student_data.get('first_name')} {student_data.get('last_name')}"
        )

        if StudentRepository.exists_by_student_number(
            student_data.get("student_number")
        ):
            logger.error(
                f"Student number {student_data.get('student_number')} already exists"
            )
            raise ValueError(
                f"Student number {student_data.get('student_number')} is already taken"
            )

        if StudentRepository.exists_by_document_number(
            student_data.get("document_number")
        ):
            logger.error(
                f"Document number {student_data.get('document_number')} already registered"
            )
            raise ValueError(
                f"Document number {student_data.get('document_number')} is already registered"
            )

        if not SpecialtyRepository.exists_by_id(student_data.get("specialty_id")):
            logger.error(
                f"Specialty with id {student_data.get('specialty_id')} not found"
            )
            raise ValueError(
                f"Specialty with id {student_data.get('specialty_id')} does not exist"
            )

        if not DocumentTypeRepository.exists_by_id(
            student_data.get("document_type_id")
        ):
            logger.error(
                f"Document type with id {student_data.get('document_type_id')} not found"
            )
            raise ValueError(
                f"Document type with id {student_data.get('document_type_id')} does not exist"
            )

        created_student = StudentRepository.create(student_data)
        logger.info(f"Student created successfully with id: {created_student.id}")
        return created_student

    @staticmethod
    def find_by_id(id: int) -> Optional[Any]:
        logger.info(f"Finding student with id: {id}")
        student = StudentRepository.find_by_id(id)
        if not student:
            logger.warning(f"Student with id {id} not found")
        return student

    @staticmethod
    def find_by_student_number(student_number: int) -> Optional[Any]:
        logger.info(f"Finding student with student number: {student_number}")
        student = StudentRepository.find_by_student_number(student_number)
        if not student:
            logger.warning(f"Student with student number {student_number} not found")
        return student

    @staticmethod
    def find_all() -> List[Any]:
        logger.info("Finding all students")
        students = StudentRepository.find_all()
        logger.info(f"Found {len(students)} students")
        return students

    @staticmethod
    def find_by_specialty(specialty_id: int) -> List[Any]:
        logger.info(f"Finding students by specialty id: {specialty_id}")

        if not SpecialtyRepository.exists_by_id(specialty_id):
            logger.error(f"Specialty with id {specialty_id} not found")
            raise ValueError(f"Specialty with id {specialty_id} does not exist")

        students = StudentRepository.find_by_specialty(specialty_id)
        logger.info(f"Found {len(students)} students in specialty {specialty_id}")
        return students

    @staticmethod
    @transaction.atomic
    def update(id: int, student_data: dict) -> Any:
        logger.info(f"Updating student with id: {id}")

        existing_student = StudentRepository.find_by_id(id)
        if not existing_student:
            logger.error(f"Student with id {id} not found for update")
            raise ValueError(f"Student with id {id} does not exist")

        student_number = student_data.get("student_number")
        if student_number and student_number != existing_student.student_number:
            if StudentRepository.exists_by_student_number(student_number):
                logger.error(f"Student number {student_number} already exists")
                raise ValueError(f"Student number {student_number} is already taken")

        document_number = student_data.get("document_number")
        if document_number and document_number != existing_student.document_number:
            if StudentRepository.exists_by_document_number(document_number):
                logger.error(f"Document number {document_number} already registered")
                raise ValueError(
                    f"Document number {document_number} is already registered"
                )

        specialty_id = student_data.get("specialty_id")
        if specialty_id and not SpecialtyRepository.exists_by_id(specialty_id):
            logger.error(f"Specialty with id {specialty_id} not found")
            raise ValueError(f"Specialty with id {specialty_id} does not exist")

        for key, value in student_data.items():
            if hasattr(existing_student, key):
                setattr(existing_student, key, value)

        updated_student = StudentRepository.update(existing_student)
        logger.info(f"Student with id {id} updated successfully")
        return updated_student

    @staticmethod
    @transaction.atomic
    def delete_by_id(id: int) -> bool:
        logger.info(f"Deleting student with id: {id}")

        if not StudentRepository.exists_by_id(id):
            logger.error(f"Student with id {id} not found for deletion")
            raise ValueError(f"Student with id {id} does not exist")

        result = StudentRepository.delete_by_id(id)
        logger.info(f"Student with id {id} deleted successfully")
        return result

    @staticmethod
    def calculate_age(student: Any) -> Optional[int]:
        if not student or not student.birth_date:
            logger.warning("Cannot calculate age: student or birth_date is None")
            return None

        today = datetime.date.today()
        age = (
            today.year
            - student.birth_date.year
            - (
                (today.month, today.day)
                < (student.birth_date.month, student.birth_date.day)
            )
        )
        logger.debug(f"Calculated age for student {student.id}: {age}")
        return age

    @staticmethod
    def is_enrollment_valid(
        birth_date: datetime.date, enrollment_date: datetime.date
    ) -> bool:
        if enrollment_date < birth_date:
            return False

        age_at_enrollment = enrollment_date.year - birth_date.year
        if (enrollment_date.month, enrollment_date.day) < (
            birth_date.month,
            birth_date.day,
        ):
            age_at_enrollment -= 1

        return age_at_enrollment >= 16

    @staticmethod
    def generate_regular_student_certificate(id: int, type: str) -> Any:
        logger.info(f"Generating certificate for student id: {id}, type: {type}")

        student = StudentRepository.find_with_full_relations(id)
        if not student:
            logger.error(f"Student with id {id} not found")
            raise ValueError(f"Student with id {id} not found")

        context = StudentService._get_student_data(student)

        document_generator = get_document_generator(type)
        if not document_generator:
            logger.error(f"Document type '{type}' is not supported")
            raise ValueError(f"Document type '{type}' is not supported")

        logger.info(f"Certificate generated successfully for student {id}")
        return document_generator.generate(
            folder="certificate", template="certificate_pdf", context=context
        )

    @staticmethod
    def _get_current_date() -> str:
        current_date = datetime.datetime.now()
        return current_date.strftime("%d de %B de %Y")

    @staticmethod
    def _get_student_data(student: Any) -> dict:
        return {
            "student": student,
            "specialty": student.specialty,
            "faculty": student.specialty.faculty,
            "university": student.specialty.faculty.university,
            "date": StudentService._get_current_date(),
        }
