from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    acronym = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        unique=True,
        help_text="Unique acronym for the university",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.acronym} - {self.name}"

    def __repr__(self):
        return f"<University: {self.acronym}>"

    class Meta:
        db_table = "universities"
        verbose_name = "University"
        verbose_name_plural = "Universities"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["acronym"]),
        ]
