from rest_framework import serializers
from app.models import Position


class PositionSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            "required": "Position name is required.",
            "blank": "Position name cannot be blank.",
            "max_length": "Position name must not exceed 50 characters.",
            "min_length": "Position name must be at least 2 characters long.",
        },
    )

    points = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=0,
        error_messages={
            "min_value": "Points must be a non-negative integer.",
            "invalid": "Points must be a valid integer.",
        },
    )

    position_category_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "Position category ID is required.",
            "invalid": "Position category ID must be a valid integer.",
        },
    )

    dedication_type_id = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "Dedication type ID is required.",
            "invalid": "Dedication type ID must be a valid integer.",
        },
    )

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError(
                "Position name cannot be only whitespace."
            )

        if not value[0].isalpha():
            raise serializers.ValidationError("Position name must start with a letter.")

        return value.strip().title()

    def validate_position_category_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Position category ID must be a positive integer."
            )

        return value

    def validate_dedication_type_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Dedication type ID must be a positive integer."
            )

        return value

    class Meta:
        model = Position
        fields = [
            "id",
            "name",
            "points",
            "position_category_id",
            "dedication_type_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
