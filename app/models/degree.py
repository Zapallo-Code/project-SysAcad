from django.db import models
from .base import BaseModel


class Degree(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "degrees"
        verbose_name = "Degree"
        verbose_name_plural = "Degrees"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
