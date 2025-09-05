from django.db import models
from .student import Student
from .subject import Subject


class SubjectInscription(models.Model):
    """
    Enrollment record for a subject (course).

    Attributes:
        student (Student): Student who enrolls in the subject.
        subject (Subject): Target subject of the enrollment.
        inscription_date (date): Creation date; auto-populated.

    Meta:
        unique_together: Ensures a student cannot enroll in the same subject twice.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subjects_inscriptions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_inscriptions')
    inscription_date = models.DateField(auto_now_add=True)

    def __str__(self):
        """Human-readable representation used in admin and logs."""
        return f"{self.student.user.username} - {self.subject.name} ({self.inscription_date})"

    class Meta:
        unique_together = ('student', 'subject')
