"""Django admin registrations for the Inscriptions app.

Registers SubjectInscription and FinalExamInscription with basic list and search configuration.
"""

from django.contrib import admin
from app.models import SubjectInscription, FinalExamInscription


@admin.register(SubjectInscription)
class SubjectInscriptionAdmin(admin.ModelAdmin):
    """Admin for SubjectInscription: student, subject and inscription date."""
    list_display = ("student", "subject", "inscription_date")
    search_fields = ("student__user__username", "subject__name", "subject__code")


@admin.register(FinalExamInscription)
class FinalExamInscriptionAdmin(admin.ModelAdmin):
    """Admin for FinalExamInscription: student, final exam and inscription date."""
    list_display = ("student", "final_exam", "inscription_date")
    search_fields = ("student__user__username", "final_exam__subject__name", "final_exam__subject__code")
