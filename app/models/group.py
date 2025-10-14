from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    
    class Meta:
        db_table = 'grupos'
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<Group: {self.name}>"
