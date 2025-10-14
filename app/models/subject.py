from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        unique=True,
        help_text="Código único identificador de la materia"
    )
    observation = models.CharField(max_length=255, null=True, blank=True)
    
    # La relación ManyToMany con Authority está definida en el modelo Authority
    # para acceder a las autoridades de una materia: subject.authorities.all()
    
    class Meta:
        db_table = 'materias'
        verbose_name = 'Materia'
        verbose_name_plural = 'Materias'
        ordering = ['code', 'name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def __repr__(self):
        return f"<Subject: {self.code} - {self.name}>"
