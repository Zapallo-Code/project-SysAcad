from django.db import models


class SpecialtyType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    level = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'tipoespecialidades'
        verbose_name = 'Tipo de Especialidad'
        verbose_name_plural = 'Tipos de Especialidades'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<SpecialtyType: {self.name}>"
