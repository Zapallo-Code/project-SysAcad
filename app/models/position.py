from django.db import models
from .base import BaseModel


class Position(BaseModel):
    name = models.CharField(max_length=50, null=False, blank=False)
    points = models.IntegerField(null=True, blank=True)

    position_category = models.ForeignKey(
        "PositionCategory",
        on_delete=models.PROTECT,
        related_name="positions",
        null=False,
    )

    dedication_type = models.ForeignKey(
        "DedicationType", on_delete=models.PROTECT, related_name="positions", null=False
    )

    def __str__(self):
        return f"{self.name} ({self.position_category})"

    class Meta(BaseModel.Meta):
        db_table = "positions"
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["position_category"]),
        ]
