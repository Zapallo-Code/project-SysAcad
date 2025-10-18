from rest_framework import serializers
from app.models import DedicationType


class DedicationTypeSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=100,
        min_length=2,
        required=True,
        error_messages={
            "required": "Dedication type name is required.",
            "blank": "Dedication type name cannot be blank.",
            "max_length": "Dedication type name must not exceed 100 characters.",
            "min_length": "Dedication type name must be at least 2 characters long.",
        },
    )

    observation = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={
            "max_length": "Observation must not exceed 200 characters.",
        },
    )

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "Dedication type name cannot be only whitespace."
            )

        if not value[0].isalpha():
            raise serializers.ValidationError(
                "Dedication type name must start with a letter."
            )

        return value.strip().title()

    class Meta:
        model = DedicationType
        fields = ["id", "name", "observation", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
