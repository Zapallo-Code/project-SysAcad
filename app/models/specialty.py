from django.db import models


class Specialty(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    letter = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        help_text="Letra identificadora de la especialidad"
    )
    observation = models.CharField(max_length=255, null=True, blank=True)
    
    specialty_type = models.ForeignKey(
        'SpecialtyType',
        on_delete=models.PROTECT,
        related_name='specialties',
        null=False
    )
    
    faculty = models.ForeignKey(
        'Faculty',
        on_delete=models.PROTECT,
        related_name='specialties',
        null=False
    )
    
    class Meta:
        db_table = 'especialidades'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['letter']),
        ]
        unique_together = [['faculty', 'letter']]
    
    def __str__(self):
        return f"{self.name} ({self.letter})"
    
    def __repr__(self):
        return f"<Specialty: {self.name} - Letter: {self.letter}>"
