from django.db import models
from .base import BaseModel


class Orientation(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)

    specialty = models.ForeignKey(
        "Specialty", on_delete=models.PROTECT, related_name="orientations", null=False
    )

    plan = models.ForeignKey(
        "Plan", on_delete=models.PROTECT, related_name="orientations", null=False
    )

    subject = models.ForeignKey(
        "Subject", on_delete=models.PROTECT, related_name="orientations", null=False
    )

    def __str__(self):
        return f"{self.name} - {self.specialty}"

    class Meta(BaseModel.Meta):
        db_table = "orientations"
        verbose_name = "Orientation"
        verbose_name_plural = "Orientations"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["specialty"]),
            models.Index(fields=["plan"]),
        ]
