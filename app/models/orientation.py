from django.db import models


class Orientation(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.PROTECT,
        related_name='orientations',
        null=False
    )

    plan = models.ForeignKey(
        'Plan',
        on_delete=models.PROTECT,
        related_name='orientations',
        null=False
    )

    subject = models.ForeignKey(
        'Subject',
        on_delete=models.PROTECT,
        related_name='orientations',
        null=False
    )

    def __str__(self):
        return f"{self.name} - {self.specialty}"

    def __repr__(self):
        return f"<Orientation: {self.name}>"
