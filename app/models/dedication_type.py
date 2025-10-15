from django.db import models


class DedicationType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    observation = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<DedicationType: {self.name}>"

    class Meta:
        db_table = 'dedication_types'
        verbose_name = 'Dedication Type'
        verbose_name_plural = 'Dedication Types'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
