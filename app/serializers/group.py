from rest_framework import serializers
from app.models import Group


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            "required": "Group name is required.",
            "blank": "Group name cannot be blank.",
            "max_length": "Group name must not exceed 50 characters.",
            "min_length": "Group name must be at least 2 characters long.",
        },
    )

    def validate_name(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError("Group name cannot be only whitespace.")

        if not value[0].isalpha():
            raise serializers.ValidationError("Group name must start with a letter.")

        return value.strip().title()

    class Meta:
        model = Group
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
