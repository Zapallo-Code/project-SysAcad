from django.db import models


class DedicationType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    observation = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        db_table = 'dedication_typees'
        verbose_name = 'Tipo de Dedicación'
        verbose_name_plural = 'Tipos de Dedicación'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<DedicationType: {self.name}>"
