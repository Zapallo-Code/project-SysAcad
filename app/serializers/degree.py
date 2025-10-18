from rest_framework import serializers
from app.models import Degree


class DegreeSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            'required': 'Degree name is required.',
            'blank': 'Degree name cannot be blank.',
            'max_length': 'Degree name must not exceed 50 characters.',
            'min_length': 'Degree name must be at least 2 characters long.',
        }
    )

    description = serializers.CharField(
        max_length=200,
        required=False,
        allow_blank=True,
        allow_null=True,
        error_messages={
            'max_length': 'Description must not exceed 200 characters.',
        }
    )

    def validate_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Degree name cannot be only whitespace.')

        if not value[0].isalpha():
            raise serializers.ValidationError('Degree name must start with a letter.')

        return value.strip().title()

    class Meta:
        model = Degree
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
