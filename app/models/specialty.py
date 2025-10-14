from django.db import models


class Specialty(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    letter = models.CharField(
        max_length=1,
        null=False,
        blank=False,
        help_text="Identifier letter for the specialty"
    )
    observation = models.CharField(max_length=255, null=True, blank=True)

    specialty_type = models.ForeignKey(
        'SpecialtyType',
        on_delete=models.PROTECT,
        related_name='specialties',
        null=False
    )

    faculty = models.ForeignKey(
        'Faculty',
        on_delete=models.PROTECT,
        related_name='specialties',
        null=False
    )

    def __str__(self):
        return f"{self.name} ({self.letter})"

    def __repr__(self):
        return f"<Specialty: {self.name} - Letter: {self.letter}>"
