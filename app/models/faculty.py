from django.db import models
from django.core.validators import EmailValidator


class Faculty(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    abbreviation = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        help_text="Faculty abbreviation"
    )
    directory = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="Directory path or location"
    )
    acronym = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        help_text="Faculty identifying acronym"
    )

    postal_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    contact_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Contact person's name"
    )
    email = models.EmailField(
        max_length=100,
        null=False,
        blank=False,
        validators=[EmailValidator(message="Please enter a valid email address")]
    )

    university = models.ForeignKey(
        'University',
        on_delete=models.PROTECT,
        related_name='faculties',
        null=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

    def __repr__(self):
        return f"<Faculty: {self.name} - {self.acronym}>"

    class Meta:
        db_table = 'faculties'
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'
        ordering = ['name']
        indexes = [
            models.Index(fields=['acronym']),
            models.Index(fields=['abbreviation']),
            models.Index(fields=['name']),
        ]
