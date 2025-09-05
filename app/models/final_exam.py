from django.db import models
from .subject import Subject


class FinalExam(models.Model):
    """
    Final exam call (session) for a Subject.

    Attributes:
        subject (Subject): Subject being examined (FK).
        date (date): Exam date.
        location (str): Where the exam takes place.
        duration (timedelta): Expected duration.
        call_number (int): Call identifier/ordinal within the period.
        notes (str | None): Optional remarks for logistics or scope.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='final_exams')
    date = models.DateField()
    location = models.CharField(max_length=255)
    duration = models.DurationField()
    call_number = models.PositiveSmallIntegerField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject.name} Final Exam on {self.date.strftime('%Y-%m-%d')}"
