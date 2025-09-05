from django.db import models
from .custom_user import CustomUser


class Administrator(models.Model):
    """
    Administrator profile for non-teaching staff.

    Attributes:
        administrator_id (str): Unique identifier (primary key).
        user (CustomUser): Related user account.
        position (str): Job position/title.
        hire_date (date): Hiring date.
    """
    administrator_id = models.CharField(max_length=20, unique=True, primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='administrator')
    position = models.CharField(max_length=100)
    hire_date = models.DateField()

    class Meta:
        """Meta options for Administrator."""
        db_table = 'administrators'

    def __str__(self):
        """Return full name for admin readability."""
        return f"{self.user.get_full_name()}"
