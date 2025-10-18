from typing import Optional, List, Dict, Any
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from app.models import Student


class StudentRepository:
    @staticmethod
    def create(student_data: Dict[str, Any]) -> Student:
        student = Student(**student_data)
        student.full_clean()
        student.save()
        return student

    @staticmethod
    def find_by_id(id: int) -> Optional[Student]:
        try:
            return Student.objects.select_related("document_type", "specialty").get(
                id=id
            )
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def find_by_student_number(student_number: int) -> Optional[Student]:
        try:
            return Student.objects.select_related("document_type", "specialty").get(
                student_number=student_number
            )
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @staticmethod
    def find_by_document_number(document_number: str) -> List[Student]:
        return list(
            Student.objects.filter(document_number=document_number).select_related(
                "document_type", "specialty"
            )
        )

    @staticmethod
    def find_all() -> List[Student]:
        return list(Student.objects.select_related("document_type", "specialty").all())

    @staticmethod
    def find_by_specialty(specialty_id: int) -> List[Student]:
        return list(
            Student.objects.filter(specialty_id=specialty_id).select_related(
                "document_type", "specialty"
            )
        )

    @staticmethod
    def find_by_gender(gender: str) -> List[Student]:
        return list(
            Student.objects.filter(gender=gender).select_related(
                "document_type", "specialty"
            )
        )

    @staticmethod
    def update(student: Student) -> Student:
        student.full_clean()
        student.save()
        return student

    @staticmethod
    def delete_by_id(id: int) -> bool:
        student = StudentRepository.find_by_id(id)
        if not student:
            return False
        student.delete()
        return True

    @staticmethod
    def exists_by_id(id: int) -> bool:
        return Student.objects.filter(id=id).exists()

    @staticmethod
    def exists_by_student_number(student_number: int) -> bool:
        return Student.objects.filter(student_number=student_number).exists()

    @staticmethod
    def exists_by_document_number(document_number: str) -> bool:
        return Student.objects.filter(document_number=document_number).exists()

    @staticmethod
    def count() -> int:
        return Student.objects.count()

    @staticmethod
    def find_with_full_relations(id: int) -> Optional[Student]:
        try:
            return Student.objects.select_related(
                "document_type",
                "specialty",
                "specialty__faculty",
                "specialty__faculty__university",
                "specialty__specialty_type",
            ).get(id=id)
        except ObjectDoesNotExist:
            return None
