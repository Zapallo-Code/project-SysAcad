import datetime
from io import BytesIO
from app.models.student import Student
from app.repositories.student_repository import StudentRepository
from app.services.documentos_office_service import PDFDocument, ODTDocument, DOCXDocument, Document, get_document_type

class StudentService:

    @staticmethod
    def create(student):
        StudentRepository.create(student)

    @staticmethod
    def find_by_id(id: int) -> Student:        
        return StudentRepository.find_by_id(id)

    @staticmethod
    def find_all() -> list[Student]:
        return StudentRepository.find_all()
    
    @staticmethod
    def update(id: int, student: Student) -> Student:
        existing_student = StudentRepository.find_by_id(id)
        if not existing_student:
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
        return StudentRepository.update(existing_student)
        
    @staticmethod
    def delete_by_id(id: int) -> bool:
        return StudentRepository.delete_by_id(id)
    
    @staticmethod
    def generar_certificado_alumno_regular(id: int,tipo: str)-> BytesIO:
        student = StudentRepository.find_by_id(id)
        if not student:
            return None
        
        context = StudentService.__get_student_data(student)
        documento = get_document_type(tipo)
        if not documento:
            return None
        
        return documento.generar(
            folder='certificado',
            template='certificado_pdf',
            context=context
        )
    
    @staticmethod
    def __get_current_date():
        current_date = datetime.datetime.now()
        date_str = current_date.strftime('%d de %B de %Y')
        return date_str

    @staticmethod
    def __get_student_data(student: Student) -> dict:
        specialty = student.specialty
        faculty = specialty.faculty
        university = faculty.university
        return{
            "student": student,
            "specialty": specialty,
            "faculty": faculty,
            "university": university,
            "date":StudentService.__get_current_date()
        }

