from django.db import models
from django.core.validators import EmailValidator


class Faculty(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    abbreviation = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        help_text="Abreviatura de la facultad"
    )
    directory = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="Ruta o ubicación del directorio"
    )
    acronym = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        help_text="Sigla identificadora de la facultad"
    )
    
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    contact_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Nombre de la persona de contacto"
    )
    email = models.EmailField(
        max_length=100,
        null=False,
        blank=False,
        validators=[EmailValidator(message="Ingrese un email válido")]
    )
    
    university = models.ForeignKey(
        'University',
        on_delete=models.PROTECT,
        related_name='faculties',
        null=False
    )
    
    # La relación ManyToMany con Authority está definida en el modelo Authority
    # para acceder a las autoridades de una facultad: faculty.authorities.all()
    
    class Meta:
        db_table = 'facultades'
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['acronym']),
            models.Index(fields=['abbreviation']),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['university', 'acronym'],
                name='unique_facultad_sigla_universidad'
            ),
            models.UniqueConstraint(
                fields=['university', 'abbreviation'],
                name='unique_facultad_abreviatura_universidad'
            ),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
    
    def __repr__(self):
        return f"<Faculty: {self.name} - {self.acronym}>"
