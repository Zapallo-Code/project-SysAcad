from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        help_text="Unique identifier code for the subject"
    )
    observation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def __repr__(self):
        return f"<Subject: {self.code} - {self.name}>"
