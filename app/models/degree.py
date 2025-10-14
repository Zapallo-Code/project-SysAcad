from django.db import models


class Degree(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=False, blank=False)
    
    class Meta:
        db_table = 'grados'
        verbose_name = 'Grado'
        verbose_name_plural = 'Grados'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Degree: {self.name}>"
