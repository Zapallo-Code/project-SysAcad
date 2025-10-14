from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Group: {self.name}>"
