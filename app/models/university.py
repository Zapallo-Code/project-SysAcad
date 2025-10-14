from django.db import models


class University(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    acronym = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        unique=True,
        help_text="Sigla identificadora de la universidad"
    )
    
    class Meta:
        db_table = 'universidades'
        verbose_name = 'Universidad'
        verbose_name_plural = 'Universidades'
        ordering = ['name']
        indexes = [
            models.Index(fields=['acronym']),
        ]
    
    def __str__(self):
        return f"{self.acronym} - {self.name}"
    
    def __repr__(self):
        return f"<University: {self.acronym}>" 
