from django.db import models
from .base import BaseModel


class PositionCategory(BaseModel):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "position_categories"
        verbose_name = "Position Category"
        verbose_name_plural = "Position Categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
