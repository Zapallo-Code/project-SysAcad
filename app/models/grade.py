from django.db import models
from .student import Student
from .subject import Subject


class Grade(models.Model):
    """
    Student performance and academic status for a Subject.

    Links a Student to a Subject, tracking promotion and final grades and a derived status.

    Attributes:
        student (Student): Student owning this record (FK).
        subject (Subject): Subject graded (FK).
        promotion_grade (Decimal | None): Continuous assessment/commission grade.
        status (str): One of StatusSubject choices (FREE, REGULAR, PROMOTED).
        final_grade (Decimal | None): Final exam grade, if applicable.
        last_updated (datetime): Auto-updated timestamp on save.
        notes (str | None): Optional comments.

    Notes:
        - Uniqueness of (student, subject) is enforced via Meta.unique_together.
        - Status transitions are maintained by update_status().
    """

    class StatusSubject(models.TextChoices):
        """Academic status of the student for the subject."""
        FREE = 'free', 'Free'
        REGULAR = 'regular', 'Regular'
        PROMOTED = 'promoted', 'Promoted'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    promotion_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=StatusSubject.choices, default=StatusSubject.REGULAR)
    final_grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} ({self.status})"

    def update_status(self):
        """
        Update and persist the status based on current final_grade.

        Logic:
            - If final_grade is not None and >= 6.0 -> PROMOTED.
            - If final_grade is not None and < 6.0 -> REGULAR.
            - If final_grade is None -> FREE.

        Side Effects:
            Saves the instance (self.save()).

        Raises:
            TypeError: If final_grade is not a number when provided.
        """
        if self.final_grade is not None:
            if self.final_grade >= 6.0:
                self.status = self.StatusSubject.PROMOTED
            else:
                self.status = self.StatusSubject.REGULAR
        else:
            self.status = self.StatusSubject.FREE
        self.save()
