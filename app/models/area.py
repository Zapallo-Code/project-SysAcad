from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Area: {self.name}>"

    class Meta:
        db_table = 'areas'
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
