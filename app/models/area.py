from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Area: {self.name}>"
