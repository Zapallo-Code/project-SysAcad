from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        help_text="Unique identifier code for the subject",
    )
    observation = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    def __repr__(self):
        return f"<Subject: {self.code} - {self.name}>"

    class Meta:
        db_table = "subjects"
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"
        ordering = ["code", "name"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
        ]
