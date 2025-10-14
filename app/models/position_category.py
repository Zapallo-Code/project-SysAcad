from django.db import models


class PositionCategory(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    
    class Meta:
        db_table = 'categoriacargos'
        verbose_name = 'Categoría de Cargo'
        verbose_name_plural = 'Categorías de Cargos'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<PositionCategory: {self.name}>"
