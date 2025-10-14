from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from app.models.student import Student


class StudentRepository:
    @staticmethod
    def find_by_id(id):
        try:
            return Student.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(student):
        student.save()
        return student
    
    @staticmethod
    def find_all():
        return Student.objects.all()
    
    @staticmethod
    def update(student) -> Student:
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
    def find_by_student_number(student_number: int):
        try:
            return Student.objects.get(student_number=student_number)
        except ObjectDoesNotExist:
            return None
    
    @staticmethod
    def find_by_document_number(document_number: str):
        return Student.objects.filter(document_number=document_number)

