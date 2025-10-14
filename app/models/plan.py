from django.db import models
from django.core.exceptions import ValidationError


class Plan(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    observation = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        db_table = 'planes'
        verbose_name = 'Plan'
        verbose_name_plural = 'Planes'
        ordering = ['-start_date']  # Más recientes primero
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['end_date']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.start_date.year} - {self.end_date.year})"
    
    def __repr__(self):
        return f"<Plan: {self.name}>"
    
    def clean(self):
        super().clean()
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError({
                    'end_date': 'La fecha de fin debe ser posterior a la fecha de inicio.'
                })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        from datetime import date
        today = date.today()
        return self.start_date <= today <= self.end_date
