from django.db import models
from datetime import date


class Student(models.Model):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    document_number = models.CharField(max_length=50, null=False, blank=False)
    
    document_type = models.ForeignKey(
        'DocumentType',
        on_delete=models.PROTECT,
        related_name='students',
        null=False
    )
    
    birth_date = models.DateField(null=False, blank=False)
    
    gender = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    )
    
    student_id_number = models.IntegerField(null=False, blank=False, unique=True)
    enrollment_date = models.DateField(null=False, blank=False)
    
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.PROTECT,
        related_name='students',
        null=False
    )
    
    
    class Meta:
        db_table = 'alumnos'
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['student_id_number']),
            models.Index(fields=['document_number']),
        ]
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name} - Legajo: {self.student_id_number}"
    
    def __repr__(self):
        return f"<Student: {self.last_name}, {self.first_name}>"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
