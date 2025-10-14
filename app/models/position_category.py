from django.db import models


class PositionCategory(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<PositionCategory: {self.name}>"
