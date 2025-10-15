from django.db import models


class Degree(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    description = models.CharField(max_length=200, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Degree: {self.name}>"

    class Meta:
        db_table = 'degrees'
        verbose_name = 'Degree'
        verbose_name_plural = 'Degrees'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
