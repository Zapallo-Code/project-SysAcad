from rest_framework import serializers
from app.models import PositionCategory


class PositionCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=30,
        min_length=2,
        required=True,
        error_messages={
            "required": "Position category name is required.",
            "blank": "Position category name cannot be blank.",
            "max_length": "Position category name must not exceed 30 characters.",
            "min_length": "Position category name must be at least 2 characters long.",
        },
    )

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "Position category name cannot be only whitespace."
            )

        if not value[0].isalpha():
            raise serializers.ValidationError(
                "Position category name must start with a letter."
            )

        return value.strip().title()

    class Meta:
        model = PositionCategory
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
