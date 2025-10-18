from rest_framework import serializers
from app.models import University


class UniversitySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'required': 'University name is required.',
            'blank': 'University name cannot be blank.',
            'max_length': 'University name must not exceed 100 characters.',
            'min_length': 'University name must be at least 3 characters long.',
        }
    )

    acronym = serializers.CharField(
        max_length=10,
        min_length=2,
        required=True,
        error_messages={
            'required': 'University acronym is required.',
            'blank': 'University acronym cannot be blank.',
            'max_length': 'Acronym must not exceed 10 characters.',
            'min_length': 'Acronym must be at least 2 characters long.',
        }
    )

    def validate_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('University name cannot be only whitespace.')

        if not value[0].isalpha():
            raise serializers.ValidationError('University name must start with a letter.')

        return value.strip().title()

    def validate_acronym(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Acronym cannot be only whitespace.')

        cleaned_value = value.strip()

        if not cleaned_value.replace(' ', '').isalpha():
            raise serializers.ValidationError('Acronym must contain only letters.')

        return cleaned_value.upper()

    class Meta:
        model = University
        fields = ['id', 'name', 'acronym', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
