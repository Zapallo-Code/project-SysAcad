from django.db import models
from .base import BaseModel


class Group(BaseModel):
    name = models.CharField(max_length=20, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        db_table = "groups"
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
