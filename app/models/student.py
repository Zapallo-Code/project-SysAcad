from django.db import models
from .career import Career
from .custom_user import CustomUser


class Student(models.Model):
    """
    Student profile linked one-to-one with a CustomUser.

    Attributes:
        student_id (str): Unique student identifier (primary key).
        user (CustomUser): Related user account.
        career (Career | None): Degree program; nullable if unset.
        enrollment_date (date): Enrollment date.
    """
    student_id = models.CharField(max_length=20, unique=True, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student')
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True, related_name='students')
    enrollment_date = models.DateField()

    class Meta:
        """Meta options for Student."""
        db_table = 'students'

    def __str__(self):
        """Readable identifier combining student_id and full name."""
        return f"Student ID {self.student_id} - {self.user.get_full_name()}"
