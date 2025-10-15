from rest_framework import serializers
from app.models.document_type import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ['id', 'dni', 'civic_card', 'enrollment_card', 'passport']
        read_only_fields = ['id']

    dni = serializers.IntegerField(min_value=1000000, max_value=99999999)
    civic_card = serializers.CharField(max_length=20, min_length=1)
    enrollment_card = serializers.CharField(max_length=20, min_length=1)
    passport = serializers.CharField(max_length=20, min_length=1)
