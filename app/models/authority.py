from django.db import models
from django.core.validators import EmailValidator
from .base import BaseModel


class Authority(BaseModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        validators=[EmailValidator(message="Please enter a valid email address")],
    )

    position = models.ForeignKey(
        "Position", on_delete=models.PROTECT, related_name="authorities", null=False
    )

    subjects = models.ManyToManyField("Subject", related_name="authorities", blank=True)

    faculties = models.ManyToManyField(
        "Faculty", related_name="authorities", blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.position}"

    class Meta(BaseModel.Meta):
        db_table = "authorities"
        verbose_name = "Authority"
        verbose_name_plural = "Authorities"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["position"]),
        ]
