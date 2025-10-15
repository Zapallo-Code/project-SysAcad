from django.db import models


class SpecialtyType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    level = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<SpecialtyType: {self.name}>"

    class Meta:
        db_table = 'specialty_types'
        verbose_name = 'Specialty Type'
        verbose_name_plural = 'Specialty Types'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
