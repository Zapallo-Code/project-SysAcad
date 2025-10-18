from datetime import date
from rest_framework import serializers
from app.models import Plan


class PlanSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            'required': 'Plan name is required.',
            'blank': 'Plan name cannot be blank.',
            'max_length': 'Plan name must not exceed 50 characters.',
            'min_length': 'Plan name must be at least 2 characters long.',
        }
    )

    start_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'Start date is required.',
            'invalid': 'Enter a valid date in format YYYY-MM-DD.',
        }
    )

    end_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'End date is required.',
            'invalid': 'Enter a valid date in format YYYY-MM-DD.',
        }
    )

    observation = serializers.CharField(
        max_length=255,
        required=False,
        allow_null=True,
        allow_blank=True,
        error_messages={
            'max_length': 'Observation must not exceed 255 characters.',
        }
    )

    def validate_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Plan name cannot be only whitespace.')

        if not value[0].isalpha():
            raise serializers.ValidationError('Plan name must start with a letter.')

        return value.strip().title()

    def validate_start_date(self, value):
        if value.year < 1900:
            raise serializers.ValidationError('Start date year must be 1900 or later.')

        return value

    def validate_end_date(self, value):
        if value.year < 1900:
            raise serializers.ValidationError('End date year must be 1900 or later.')

        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError({
                                        'end_date': 'End date must be after start date.'
                })

            duration_years = (end_date - start_date).days / 365.25
            if duration_years > 20:
                raise serializers.ValidationError({
                    'end_date': 'Plan duration cannot exceed 20 years.'
                })

        return data

    class Meta:
        model = Plan
        fields = ['id', 'name', 'start_date', 'end_date', 'observation',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
