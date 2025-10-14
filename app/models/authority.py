from django.db import models
from django.core.validators import EmailValidator


class Authority(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        validators=[EmailValidator(message="Ingrese un email válido")]
    )
    
    position = models.ForeignKey(
        'Position',
        on_delete=models.PROTECT,
        related_name='authorities',
        null=False
    )
    
    subjects = models.ManyToManyField(
        'Subject',
        related_name='authorities',
        db_table='autoridades_materias',
        blank=True
    )
    
    faculties = models.ManyToManyField(
        'Faculty',
        related_name='authorities',
        db_table='facultades_autoridades',
        blank=True
    )
    
    class Meta:
        db_table = 'autoridades'
        verbose_name = 'Autoridad'
        verbose_name_plural = 'Autoridades'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.position}"
    
    def __repr__(self):
        return f"<Authority: {self.name}>"
    
    def associate_subject(self, subject):
        self.subjects.add(subject)
    
    def disassociate_subject(self, subject):
        self.subjects.remove(subject)
    
    def associate_faculty(self, faculty):
        self.faculties.add(faculty)
    
    def disassociate_faculty(self, faculty):
        self.faculties.remove(faculty)
