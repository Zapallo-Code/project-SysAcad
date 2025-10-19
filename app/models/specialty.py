from django.db import models
from .base import BaseModel


class Specialty(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    letter = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        help_text="Identifier letter for the specialty",
    )
    observation = models.CharField(max_length=255, null=True, blank=True)

    specialty_type = models.ForeignKey(
        "SpecialtyType",
        on_delete=models.PROTECT,
        related_name="specialties",
        null=False,
    )

    faculty = models.ForeignKey(
        "Faculty", on_delete=models.PROTECT, related_name="specialties", null=False
    )

    def __str__(self):
        return f"{self.name} ({self.letter})"

    class Meta(BaseModel.Meta):
        db_table = "specialties"
        verbose_name = "Specialty"
        verbose_name_plural = "Specialties"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["letter"]),
            models.Index(fields=["name"]),
            models.Index(fields=["specialty_type"]),
        ]
