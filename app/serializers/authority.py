import re
from rest_framework import serializers
from app.models import Authority


class AuthoritySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            'required': 'Authority name is required.',
            'blank': 'Authority name cannot be blank.',
            'max_length': 'Authority name must not exceed 100 characters.',
            'min_length': 'Authority name must be at least 3 characters long.',
        }
    )

    phone = serializers.CharField(
        max_length=20,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            'max_length': 'Phone number must not exceed 20 characters.',
        }
    )

    email = serializers.EmailField(
        max_length=100,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            'max_length': 'Email must not exceed 100 characters.',
            'invalid': 'Enter a valid email address.',
        }
    )

    position_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Position ID is required.',
            'invalid': 'Position ID must be a valid integer.',
        }
    )

    def validate_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Authority name cannot be only whitespace.')

        if not value[0].isalpha():
            raise serializers.ValidationError('Authority name must start with a letter.')

        if not re.match(r"^[a-zA-Z\s\-']+$", value):
            raise serializers.ValidationError("Name must contain only letters, spaces, hyphens, or apostrophes.")

        return value.strip().title()

    def validate_phone(self, value):
        if not value or not value.strip():
            return value


        cleaned = value.strip()

        digits_only = cleaned.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')

        if not digits_only.isdigit():
            raise serializers.ValidationError('Phone must contain only numbers and formatting characters (spaces, hyphens, parentheses, +).')

        if len(digits_only) < 7:
            raise serializers.ValidationError('Phone number must have at least 7 digits.')

        if len(digits_only) > 15:
            raise serializers.ValidationError('Phone number cannot exceed 15 digits.')

        return cleaned

    def validate_email(self, value):
        if not value or not value.strip():
            return value

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        cleaned = value.strip()

        if not re.match(email_pattern, cleaned):
            raise serializers.ValidationError('Enter a valid email address.')

        return cleaned.lower()

    def validate_position_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('Position ID must be a positive integer.')

        return value

    class Meta:
        model = Authority
        fields = ['id', 'name', 'phone', 'email', 'position_id',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
