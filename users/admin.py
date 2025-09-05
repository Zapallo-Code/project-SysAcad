"""Django admin registrations for the Users app.

Registers CustomUser, Student, Professor, and Administrator with basic list and search configuration.

Notes:
    Uses namespaced search_fields for related user and career lookups.
"""

from django.contrib import admin
from app.models import CustomUser, Student, Professor, Administrator


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Admin for CustomUser: username, role, DNI, and email."""
    list_display = ("username", "role", "dni", "email")
    search_fields = ("username", "dni", "email")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin for Student: identity, career, and enrollment date."""
    list_display = ("student_id", "user", "career", "enrollment_date")
    search_fields = ("student_id", "user__username", "career__name")


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    """Admin for Professor: identity, degree, category, and hire date."""
    list_display = ("professor_id", "user", "degree", "category", "hire_date")
    search_fields = ("professor_id", "user__username", "degree")


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    """Admin for Administrator: identity, position, and hire date."""
    list_display = ("administrator_id", "user", "position", "hire_date")
    search_fields = ("administrator_id", "user__username", "position")
