from django.db import models


class DedicationType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    observation = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<DedicationType: {self.name}>"
