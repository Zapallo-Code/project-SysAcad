from app.models.student import Student
from app.models.area import Area
from app.models.authority import Authority
from app.models.position import Position
from app.models.position_category import PositionCategory
from app.models.department import Department
from app.models.specialty import Specialty
from app.models.faculty import Faculty
from app.models.degree import Degree
from app.models.group import Group
from app.models.subject import Subject
from app.models.orientation import Orientation
from app.models.plan import Plan
from app.models.dedication_type import DedicationType
from app.models.document_type import DocumentType
from app.models.specialty_type import SpecialtyType
from app.models.university import University
from datetime import date

from app.services.student import StudentService
from app.services.area import AreaService
from app.services.authority import AuthorityService
from app.services.position import PositionService
from app.services.position_category import PositionCategoryService
from app.services.department import DepartmentService
from app.services.specialty import SpecialtyService
from app.services.faculty import FacultyService
from app.services.degree import DegreeService
from app.services.group import GroupService
from app.services.subject import SubjectService
from app.services.orientation import OrientationService
from app.services.plan import PlanService
from app.services.dedication_type import DedicationTypeService
from app.services.document_type import DocumentTypeService
from app.services.specialty_type import SpecialtyTypeService
from app.services.university import UniversityService

def new_document_type(dni=46291002, civic_card="nacional", enrollment_card="naci", passport="nacnal"):
    document_type = DocumentType()
    document_type.dni = dni
    document_type.civic_card = civic_card
    document_type.enrollment_card = enrollment_card
    document_type.passport = passport
    DocumentTypeService.create(document_type)
    return document_type

def new_dedication_type(name="Full Dedication", observation="Test observation"):
    dt = DedicationType()
    dt.name = name
    dt.observation = observation
    DedicationTypeService.create(dt)
    return dt

def new_position_category(name="Teacher"):
    category = PositionCategory()
    category.name = name
    PositionCategoryService.create(category)
    return category

def new_position(name="Professor", points=10, position_category=None, dedication_type=None):
    position = Position()
    position.name = name
    position.points = points
    position.position_category = position_category or new_position_category()
    position.dedication_type = dedication_type or new_dedication_type()
    PositionService.create(position)
    return position

def new_faculty(name="Faculty of Sciences", abbreviation="FSC", directory="/faculty/sciences",
                acronym="FS", postal_code="12345", city="City", address="Street 123",
                phone="123456789", contact_name="John Doe", email="1234@gmail.com", university=None, authorities=None):
    faculty = Faculty()
    faculty.name = name
    faculty.abbreviation = abbreviation
    faculty.directory = directory
    faculty.acronym = acronym
    faculty.postal_code = postal_code
    faculty.city = city
    faculty.address = address
    faculty.phone = phone
    faculty.contact_name = contact_name
    faculty.email = email
    faculty.university = university or new_university()

    FacultyService.create(faculty)
    
    # Asignar autoridades después de crear la facultad
    if authorities is None:
        authorities = []
    if authorities:
        faculty.authorities.set(authorities)
    
    return faculty

def new_department(name="Mathematics"):
    department = Department()
    department.name = name
    DepartmentService.create(department)
    return department

def new_area(name="Mathematics"):
    area = Area()
    area.name = name
    AreaService.create(area)
    return area

def new_specialty_type(name="Cardiology", level="Advanced"):
    specialty_type = SpecialtyType()
    specialty_type.name = name
    specialty_type.level = level
    SpecialtyTypeService.create(specialty_type)
    return specialty_type

def new_specialty(name="Mathematics", letter="A", observation="Test observation", specialty_type=None, faculty=None):
    specialty = Specialty()
    specialty.name = name
    specialty.letter = letter
    specialty.observation = observation
    specialty.specialty_type = specialty_type or new_specialty_type()
    specialty.faculty = faculty or new_faculty()
    SpecialtyService.create(specialty)
    return specialty

def new_plan(name="Plan A", start_date=date(2024, 6, 4), end_date=date(2024, 6, 5), observation="Test observation"):
    plan = Plan()
    plan.name = name
    plan.start_date = start_date
    plan.end_date = end_date
    plan.observation = observation
    PlanService.create(plan)
    return plan

def new_subject(name="Mathematics", code=None, observation="Test observation", authorities=None):
    import random
    if code is None:
        code = f"MAT{random.randint(1000, 9999)}"
    
    subject = Subject()
    subject.name = name
    subject.code = code
    subject.observation = observation
    
    SubjectService.create(subject)
    
    # Asignar autoridades después de crear la materia
    if authorities is None:
        authorities = []
    if authorities:
        subject.authorities.set(authorities)
    
    return subject

def new_orientation(name="Orientation 1", specialty=None, plan=None, subject=None):
    orientation = Orientation()
    orientation.name = name
    orientation.specialty = specialty or new_specialty()
    orientation.plan = plan or new_plan()
    orientation.subject = subject or new_subject()
    OrientationService.create(orientation)
    return orientation

def new_university(name="National University", acronym=None):
    import random
    if acronym is None:
        acronym = f"UN{random.randint(100, 999)}"
    
    university = University()
    university.name = name
    university.acronym = acronym
    UniversityService.create(university)
    return university

def new_degree(name="First", description="Description of the first degree"):
    degree = Degree()
    degree.name = name
    degree.description = description
    DegreeService.create(degree)
    return degree

def new_group(name="Group A"):
    group = Group()
    group.name = name
    GroupService.create(group)
    return group

def new_student(first_name="Juan", last_name="Pérez", document_number="46291002", document_type=None,
                birth_date=date(1990, 1, 1), gender="M", student_number=123456, enrollment_date=date(2020, 1, 1), specialty=None):
    student = Student()
    student.first_name = first_name
    student.last_name = last_name
    student.document_number = document_number
    student.document_type = document_type or new_document_type()
    student.birth_date = birth_date
    student.gender = gender
    student.student_number = student_number
    student.enrollment_date = enrollment_date
    student.specialty = specialty or new_specialty()
    StudentService.create(student)
    return student

def new_authority(name="Pelo", position=None, phone="123456789", email="123@gmail.com", 
                   subjects=None, faculties=None):
    authority = Authority()
    authority.name = name
    authority.position = position or new_position()
    authority.phone = phone
    authority.email = email

    AuthorityService.create(authority)
    
    # Asignar materias y facultades después de crear la authority
    if subjects is None:
        subjects = []
    if subjects:
        authority.subjects.set(subjects)

    if faculties is None:
        faculties = []
    if faculties:
        authority.faculties.set(faculties)
    
    return authority
