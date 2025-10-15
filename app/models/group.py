from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Group: {self.name}>"

    class Meta:
        db_table = 'groups'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
