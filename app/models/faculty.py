from django.db import models


class Faculty(models.Model):
    """
    Academic faculty or school within the institution.

    Attributes:
        name (str): Human-readable name.
        code (str): Unique short code (primary key).
        address (str): Postal address.
        phone (str): Contact phone number.
        email (str): Official contact email.
        website (str): Public website URL.
        dean (str): Dean or authority in charge.
        established_date (date): Founding or establishment date.
        description (str | None): Optional free-form notes.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, primary_key=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    dean = models.CharField(max_length=100)
    established_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
