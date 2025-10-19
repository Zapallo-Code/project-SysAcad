from django.db import models
from .base import BaseModel


class Department(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "departments"
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
