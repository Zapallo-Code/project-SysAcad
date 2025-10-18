from rest_framework import serializers
from app.models import DocumentType


class DocumentTypeSerializer(serializers.ModelSerializer):

    dni = serializers.IntegerField(
        required=True,
        min_value=1000000,
        max_value=99999999,
        error_messages={
            'required': 'DNI is required.',
            'min_value': 'DNI must be at least 7 digits.',
            'max_value': 'DNI cannot exceed 8 digits.',
            'invalid': 'DNI must be a valid integer.',
        }
    )

    civic_card = serializers.CharField(
        max_length=20,
        min_length=1,
        required=True,
        error_messages={
            'required': 'Civic card is required.',
            'blank': 'Civic card cannot be blank.',
            'max_length': 'Civic card must not exceed 20 characters.',
        }
    )

    enrollment_card = serializers.CharField(
        max_length=20,
        min_length=1,
        required=True,
        error_messages={
            'required': 'Enrollment card is required.',
            'blank': 'Enrollment card cannot be blank.',
            'max_length': 'Enrollment card must not exceed 20 characters.',
        }
    )

    passport = serializers.CharField(
        max_length=20,
        min_length=1,
        required=True,
        error_messages={
            'required': 'Passport is required.',
            'blank': 'Passport cannot be blank.',
            'max_length': 'Passport must not exceed 20 characters.',
        }
    )

    def validate_civic_card(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Civic card cannot be only whitespace.')
        return value.strip().upper()

    def validate_enrollment_card(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Enrollment card cannot be only whitespace.')
        return value.strip().upper()

    def validate_passport(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Passport cannot be only whitespace.')
        return value.strip().upper()

    class Meta:
        model = DocumentType
        fields = ['id', 'dni', 'civic_card', 'enrollment_card', 'passport', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
