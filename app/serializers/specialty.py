from rest_framework import serializers
from app.models import Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        min_length=3,
        required=True,
        error_messages={
            "required": "Specialty name is required.",
            "blank": "Specialty name cannot be blank.",
            "max_length": "Specialty name must not exceed 100 characters.",
            "min_length": "Specialty name must be at least 3 characters long.",
        },
    )

    letter = serializers.CharField(
        max_length=1,
        min_length=1,
        required=True,
        error_messages={
            "required": "Specialty letter is required.",
            "blank": "Letter cannot be blank.",
            "max_length": "Letter must be exactly 1 character.",
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

    specialty_type_id = serializers.IntegerField(
        required=True,
        source="specialty_type.id",
        error_messages={
            "required": "Specialty type ID is required.",
            "invalid": "Specialty type ID must be a valid integer.",
        },
    )

    faculty_id = serializers.IntegerField(
        required=True,
        source="faculty.id",
        error_messages={
            "required": "Faculty ID is required.",
            "invalid": "Faculty ID must be a valid integer.",
        },
    )

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "Specialty name cannot be only whitespace."
            )

        if not value[0].isalpha():
            raise serializers.ValidationError(
                "Specialty name must start with a letter."
            )

        return value.strip().title()

    def validate_letter(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Letter cannot be only whitespace.")

        cleaned = value.strip().upper()
        if not cleaned.isalpha() or len(cleaned) != 1:
            raise serializers.ValidationError(
                "Letter must be a single alphabetic character."
            )

        return cleaned

    def validate_specialty_type_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Specialty type ID must be a positive integer."
            )

        return value

    def validate_faculty_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Faculty ID must be a positive integer.")

        return value

    class Meta:
        model = Specialty
        fields = [
            "id",
            "name",
            "letter",
            "observation",
            "specialty_type_id",
            "faculty_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
