from django.db import models
from .faculty import Faculty


class Career(models.Model):
    """
    Academic program (degree) offered by a Faculty.

    Attributes:
        name (str): Program name.
        code (str): Unique program code (primary key).
        faculty (Faculty): Owning faculty (FK).
        director (str): Program director.
        duration_years (int): Nominal duration in years.
        description (str | None): Optional description.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, primary_key=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='careers')
    director = models.CharField(max_length=100)
    duration_years = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.faculty.name}"
