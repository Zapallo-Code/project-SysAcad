from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    
    class Meta:
        db_table = 'areas'
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Area: {self.name}>"
    
