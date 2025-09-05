from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user extending AbstractUser with roles and identity fields.

    Attributes:
        role (str): One of Role choices: {'administrator', 'professor', 'student'}.
        dni (str): National ID; unique.
        phone (str | None): Optional phone number.
        birth_date (date | None): Optional birth date.
        address (str | None): Optional address.
    """

    class Role(models.TextChoices):
        """User roles in the system."""
        ADMIN = 'administrator', 'Administrator'
        PROFESSOR = 'professor', 'Professor'
        STUDENT = 'student', 'Student'

    role = models.CharField(max_length=20, choices=Role.choices, blank=False, null=False)
    dni = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        """Meta options for CustomUser."""
        db_table = 'users'

    def __str__(self):
        """Return full name for admin readability."""
        return f"{self.get_full_name()}"
