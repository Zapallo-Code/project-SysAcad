import re
from rest_framework import serializers
from app.models import Faculty


class FacultySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'required': 'Faculty name is required.',
            'blank': 'Faculty name cannot be blank.',
            'max_length': 'Faculty name must not exceed 100 characters.',
            'min_length': 'Faculty name must be at least 3 characters long.',
        }
    )

    abbreviation = serializers.CharField(
        max_length=10,
        min_length=2,
        required=True,
        error_messages={
            'required': 'Faculty abbreviation is required.',
            'blank': 'Abbreviation cannot be blank.',
            'max_length': 'Abbreviation must not exceed 10 characters.',
        }
    )

    directory = serializers.CharField(
        max_length=100,
        min_length=1,
        required=True,
        error_messages={
            'required': 'Directory is required.',
            'max_length': 'Directory must not exceed 100 characters.',
        }
    )

    acronym = serializers.CharField(
        max_length=10,
        min_length=2,
        required=True,
        error_messages={
            'required': 'Acronym is required.',
            'blank': 'Acronym cannot be blank.',
            'max_length': 'Acronym must not exceed 10 characters.',
        }
    )

    postal_code = serializers.CharField(
        max_length=10,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    city = serializers.CharField(
        max_length=50,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    address = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    contact_name = serializers.CharField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True
    )

    email = serializers.EmailField(
        max_length=100,
        required=True,
        error_messages={
            'required': 'Email is required.',
            'invalid': 'Enter a valid email address.',
        }
    )

    university_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'University ID is required.',
            'invalid': 'University ID must be a valid integer.',
        }
    )

    def validate_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Faculty name cannot be only whitespace.')

        if not value[0].isalpha():
            raise serializers.ValidationError('Faculty name must start with a letter.')

        return value.strip().title()

    def validate_abbreviation(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Abbreviation cannot be only whitespace.')

        return value.strip().upper()

    def validate_acronym(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Acronym cannot be only whitespace.')

        cleaned = value.strip()
        if not cleaned.replace(' ', '').isalpha():
            raise serializers.ValidationError('Acronym must contain only letters.')

        return cleaned.upper()

    def validate_email(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Email cannot be only whitespace.')

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value.strip()):
            raise serializers.ValidationError('Enter a valid email address.')

        return value.strip().lower()

    def validate_phone(self, value):
        if value and value.strip():
            cleaned = value.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not cleaned.isdigit():
                raise serializers.ValidationError('Phone must contain only numbers, spaces, hyphens, or parentheses.')

        return value

    def validate_university_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('University ID must be a positive integer.')

        return value

    class Meta:
        model = Faculty
        fields = ['id', 'name', 'abbreviation', 'directory', 'acronym', 'postal_code',
                  'city', 'address', 'phone', 'contact_name', 'email', 'university_id',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
