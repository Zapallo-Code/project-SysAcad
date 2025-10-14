from django.db import models


class DocumentType(models.Model):
    dni = models.IntegerField(
        null=False,
        blank=False,
        help_text="Type: DNI (Documento Nacional de Identidad)"
    )
    civic_card = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="Type: L.C (Libreta Cívica)"
    )
    enrollment_card = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="Type: L.E (Libreta de Enrolamiento)"
    )
    passport = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        help_text="Type: Pasaporte"
    )

    def __str__(self):
        types = []
        if self.dni:
            types.append(f"DNI: {self.dni}")
        if self.civic_card:
            types.append(f"L.C: {self.civic_card}")
        if self.enrollment_card:
            types.append(f"L.E: {self.enrollment_card}")
        if self.passport:
            types.append(f"Pasaporte: {self.passport}")
        return " | ".join(types) if types else "Tipo de Documento"

    def __repr__(self):
        return f"<DocumentType: id={self.id}>"
