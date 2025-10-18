import re
from rest_framework import serializers
from app.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        min_length=3,
        required=True,
        error_messages={
            "required": "Subject name is required.",
            "blank": "Subject name cannot be blank.",
            "max_length": "Subject name must not exceed 255 characters.",
            "min_length": "Subject name must be at least 3 characters long.",
        },
    )

    code = serializers.CharField(
        max_length=20,
        min_length=2,
        required=True,
        error_messages={
            "required": "Subject code is required.",
            "blank": "Subject code cannot be blank.",
            "max_length": "Subject code must not exceed 20 characters.",
            "min_length": "Subject code must be at least 2 characters long.",
        },
    )

    observation = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            "max_length": "Observation must not exceed 255 characters.",
        },
    )

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Subject name cannot be only whitespace.")

        if not value[0].isalpha():
            raise serializers.ValidationError("Subject name must start with a letter.")

        return value.strip().title()

    def validate_code(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Subject code cannot be only whitespace.")

        cleaned = value.strip()

        if not re.match(r"^[A-Za-z0-9_-]+$", cleaned):
            raise serializers.ValidationError(
                "Subject code must contain only letters, numbers, hyphens, or underscores."
            )

        return cleaned.upper()

    class Meta:
        model = Subject
        fields = ["id", "name", "code", "observation", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
