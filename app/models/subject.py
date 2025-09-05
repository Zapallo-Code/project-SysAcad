from django.db import models
from .career import Career


class Subject(models.Model):
    """
    Course within a Career curriculum.

    Attributes:
        name (str): Course name.
        code (str): Unique subject code (primary key).
        career (Career): Career this subject belongs to (FK).
        year (int): Recommended year in the plan.
        category (str): One of Category choices.
        period (str): One of Period choices.
        semanal_hours (int): Weekly contact hours.
        description (str | None): Optional description.
    """

    class Category(models.TextChoices):
        """Category options for curriculum classification."""
        OBLIGATORY = 'obligatory', 'Obligatory'
        ELECTIVE = 'elective', 'Elective'

    class Period(models.TextChoices):
        """Academic period options."""
        FIRST = 'first', 'First'
        SECOND = 'second', 'Second'
        ANNUAL = 'annual', 'Annual'

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, primary_key=True)
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='subjects')
    year = models.PositiveSmallIntegerField()
    category = models.CharField(max_length=10, choices=Category.choices)
    period = models.CharField(max_length=10, choices=Period.choices)
    semanal_hours = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.career.name}"
