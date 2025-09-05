from django.db import models
from .custom_user import CustomUser
from .subject import Subject
from .final_exam import FinalExam


class Professor(models.Model):
    """
    Professor profile with subjects/final exams assignments.

    Attributes:
        professor_id (str): Unique professor identifier (primary key).
        user (CustomUser): Related user account.
        subjects (QuerySet[Subject]): Taught subjects (M2M).
        final_exams (QuerySet[FinalExam]): Assigned final exams (M2M).
        degree (str): Academic degree.
        hire_date (date): Hiring date.
        category (str): One of Category choices.
    """

    class Category(models.TextChoices):
        """Category choices for professors."""
        TITULAR = 'titular', 'Titular'
        ADJUNCT = 'adjunct', 'Adjunct'
        AUXILIAR = 'auxiliar', 'Auxiliar'

    professor_id = models.CharField(max_length=20, unique=True, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='professor')
    subjects = models.ManyToManyField(Subject, related_name='professors', blank=True)
    final_exams = models.ManyToManyField(FinalExam, related_name='professors', blank=True)
    degree = models.CharField(max_length=100)
    hire_date = models.DateField()
    category = models.CharField(max_length=20, choices=Category.choices)

    class Meta:
        """Meta options for Professor."""
        db_table = 'professors'

    def __str__(self):
        """Return full name for admin readability."""
        return f"{self.user.get_full_name()}"
