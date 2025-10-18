from django.contrib import admin
from app.models.university import University
from app.models.area import Area
from app.models.student import Student
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


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "acronym"]
    search_fields = ["name", "acronym"]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        "student_number",
        "first_name",
        "last_name",
        "document_number",
        "enrollment_date",
        "get_age",
    ]
    search_fields = ["first_name", "last_name", "document_number", "student_id"]
    list_filter = ["gender", "specialty", "enrollment_date"]

    @admin.display(description="Age")
    def get_age(self, obj):
        """Display age using Service Layer."""
        from app.services.student import StudentService

        return StudentService.calculate_age(obj)


@admin.register(Authority)
class AuthorityAdmin(admin.ModelAdmin):
    list_display = ["name", "position", "email", "phone"]
    search_fields = ["name", "email"]
    list_filter = ["position"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["name", "position_category", "dedication_type", "points"]
    search_fields = ["name"]
    list_filter = ["position_category", "dedication_type"]


@admin.register(PositionCategory)
class PositionCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ["name", "letter", "faculty", "specialty_type"]
    search_fields = ["name", "letter"]
    list_filter = ["faculty", "specialty_type"]


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ["name", "acronym", "university", "city", "email"]
    search_fields = ["name", "acronym", "city"]
    list_filter = ["university"]


@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    search_fields = ["code", "name"]


@admin.register(Orientation)
class OrientationAdmin(admin.ModelAdmin):
    list_display = ["name", "specialty", "plan", "subject"]
    search_fields = ["name"]
    list_filter = ["specialty", "plan"]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "get_is_active"]
    search_fields = ["name"]
    list_filter = ["start_date", "end_date"]

    @admin.display(description="Active", boolean=True)
    def get_is_active(self, obj):
        """Display active status using Service Layer."""
        from app.services.plan import PlanService

        return PlanService.is_plan_active(obj)


@admin.register(DedicationType)
class DedicationTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "observation"]
    search_fields = ["name"]


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "dni", "civic_card"]


@admin.register(SpecialtyType)
class SpecialtyTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]
