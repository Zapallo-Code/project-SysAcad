from rest_framework import serializers
from app.models import Orientation


class OrientationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            "required": "Orientation name is required.",
            "blank": "Orientation name cannot be blank.",
            "max_length": "Orientation name must not exceed 50 characters.",
            "min_length": "Orientation name must be at least 2 characters long.",
        },
    )

    specialty_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "Specialty ID is required.",
            "invalid": "Specialty ID must be a valid integer.",
        },
    )

    plan_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "Plan ID is required.",
            "invalid": "Plan ID must be a valid integer.",
        },
    )

    subject_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "Subject ID is required.",
            "invalid": "Subject ID must be a valid integer.",
        },
    )

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "Orientation name cannot be only whitespace."
            )

        if not value[0].isalpha():
            raise serializers.ValidationError(
                "Orientation name must start with a letter."
            )

        return value.strip().title()

    def validate_specialty_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Specialty ID must be a positive integer."
            )

        return value

    def validate_plan_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Plan ID must be a positive integer.")

        return value

    def validate_subject_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Subject ID must be a positive integer.")

        return value

    class Meta:
        model = Orientation
        fields = [
            "id",
            "name",
            "specialty_id",
            "plan_id",
            "subject_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
