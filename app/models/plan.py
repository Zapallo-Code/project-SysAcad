from django.db import models


class Plan(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    observation = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.start_date.year} - {self.end_date.year})"

    def __repr__(self):
        return f"<Plan: {self.name}>"

    @property
    def is_active(self):
        from datetime import date
        today = date.today()
        return self.start_date <= today <= self.end_date
