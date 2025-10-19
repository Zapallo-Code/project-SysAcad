from django.db import models
from .base import BaseModel


class DedicationType(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    observation = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "dedication_types"
        verbose_name = "Dedication Type"
        verbose_name_plural = "Dedication Types"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
