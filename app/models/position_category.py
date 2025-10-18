from django.db import models


class PositionCategory(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<PositionCategory: {self.name}>"

    class Meta:
        db_table = "position_categories"
        verbose_name = "Position Category"
        verbose_name_plural = "Position Categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
