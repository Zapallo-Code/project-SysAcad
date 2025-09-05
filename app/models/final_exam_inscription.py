from django.db import models
from .final_exam import FinalExam
from .student import Student


class FinalExamInscription(models.Model):
    """
    Enrollment record for a final exam session.

    Attributes:
        student (Student): Student who enrolls in the final exam.
        final_exam (FinalExam): Final exam session being enrolled.
        inscription_date (date): Creation date; auto-populated.

    Meta:
        unique_together: Ensures a student cannot enroll in the same final exam twice.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='final_exam_inscriptions')
    final_exam = models.ForeignKey(FinalExam, on_delete=models.CASCADE, related_name='final_exam_inscriptions')
    inscription_date = models.DateField(auto_now_add=True)

    def __str__(self):
        """Human-readable representation used in admin and logs."""
        return f"{self.student.user.username} - {self.final_exam.subject.name} ({self.inscription_date})"

    class Meta:
        unique_together = ('student', 'final_exam')
