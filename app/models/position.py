from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    points = models.IntegerField(null=True, blank=True)

    position_category = models.ForeignKey(
        'PositionCategory',
        on_delete=models.PROTECT,
        related_name='positions',
        null=False
    )

    dedication_type = models.ForeignKey(
        'DedicationType',
        on_delete=models.PROTECT,
        related_name='positions',
        null=False
    )

    def __str__(self):
        return f"{self.name} ({self.position_category})"

    def __repr__(self):
        return f"<Position: {self.name} - {self.points} points>"
