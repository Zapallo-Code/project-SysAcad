from django.db import models
from .base import BaseModel


class SpecialtyType(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    level = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "specialty_types"
        verbose_name = "Specialty Type"
        verbose_name_plural = "Specialty Types"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
