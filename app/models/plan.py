from django.db import models
from django.core.exceptions import ValidationError
from .base import BaseModel


class Plan(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    observation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.start_date.year} - {self.end_date.year})"

    def clean(self):
        super().clean()

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({"end_date": "End date must be after start date."})

    class Meta(BaseModel.Meta):
        db_table = "plans"
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["-start_date"]
        indexes = [
            models.Index(fields=["start_date", "end_date"]),
            models.Index(fields=["name"]),
        ]
