from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    
    class Meta:
        db_table = 'departamentos'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Department: {self.name}>"
