from django.db import models
from .base import BaseModel


class Area(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "areas"
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
