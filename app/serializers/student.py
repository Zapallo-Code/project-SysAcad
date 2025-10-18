from datetime import date, timedelta
from rest_framework import serializers
from app.models import Student


class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            'required': 'First name is required.',
            'blank': 'First name cannot be blank.',
            'max_length': 'First name must not exceed 50 characters.',
            'min_length': 'First name must be at least 2 characters long.',
        }
    )

    last_name = serializers.CharField(
        max_length=50,
        min_length=2,
        required=True,
        error_messages={
            'required': 'Last name is required.',
            'blank': 'Last name cannot be blank.',
            'max_length': 'Last name must not exceed 50 characters.',
            'min_length': 'Last name must be at least 2 characters long.',
        }
    )

    document_number = serializers.CharField(
        max_length=50,
        min_length=5,
        required=True,
        error_messages={
            'required': 'Document number is required.',
            'blank': 'Document number cannot be blank.',
            'max_length': 'Document number must not exceed 50 characters.',
            'min_length': 'Document number must be at least 5 characters long.',
        }
    )

    document_type_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Document type ID is required.',
            'invalid': 'Document type ID must be a valid integer.',
        }
    )

    birth_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'Birth date is required.',
            'invalid': 'Enter a valid birth date in format YYYY-MM-DD.',
        }
    )

    gender = serializers.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        required=True,
        error_messages={
            'required': 'Gender is required.',
            'invalid_choice': 'Gender must be M (Male), F (Female), or O (Other).',
        }
    )

    student_number = serializers.IntegerField(
        required=True,
        min_value=1,
        error_messages={
            'required': 'Student number is required.',
            'invalid': 'Student number must be a valid integer.',
            'min_value': 'Student number must be a positive integer.',
        }
    )

    enrollment_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'Enrollment date is required.',
            'invalid': 'Enter a valid enrollment date in format YYYY-MM-DD.',
        }
    )

    specialty_id = serializers.IntegerField(
        required=True,
        error_messages={
            'required': 'Specialty ID is required.',
            'invalid': 'Specialty ID must be a valid integer.',
        }
    )

    def validate_first_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('First name cannot be only whitespace.')

        if not value[0].isalpha():
            raise serializers.ValidationError('First name must start with a letter.')

        if not value.replace(' ', '').replace('-', '').isalpha():
            raise serializers.ValidationError('First name must contain only letters, spaces, or hyphens.')

        return value.strip().title()

    def validate_last_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Last name cannot be only whitespace.')

        if not value[0].isalpha():
            raise serializers.ValidationError('Last name must start with a letter.')

        if not value.replace(' ', '').replace('-', '').isalpha():
            raise serializers.ValidationError('Last name must contain only letters, spaces, or hyphens.')

        return value.strip().title()

    def validate_document_number(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError('Document number cannot be only whitespace.')

        cleaned = value.strip().replace('.', '').replace('-', '').replace(' ', '')

        if not cleaned.isalnum():
            raise serializers.ValidationError('Document number must contain only alphanumeric characters.')

        return value.strip()

    def validate_birth_date(self, value):
        today = date.today()

        if value > today:
            raise serializers.ValidationError('Birth date cannot be in the future.')

        age = (today - value).days / 365.25

        if age < 10:
            raise serializers.ValidationError('Student must be at least 10 years old.')

        if age > 120:
            raise serializers.ValidationError('Birth date is too far in the past.')

        return value

    def validate_enrollment_date(self, value):
        today = date.today()
        one_year_future = today + timedelta(days=365)
        fifty_years_ago = today - timedelta(days=365 * 50)

        if value > one_year_future:
            raise serializers.ValidationError('Enrollment date cannot be more than 1 year in the future.')

        if value < fifty_years_ago:
            raise serializers.ValidationError('Enrollment date cannot be more than 50 years in the past.')

        return value

    def validate_document_type_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('Document type ID must be a positive integer.')

        return value

    def validate_specialty_id(self, value):
        if value <= 0:
            raise serializers.ValidationError('Specialty ID must be a positive integer.')

        return value

    def validate(self, data):
        birth_date = data.get('birth_date')
        enrollment_date = data.get('enrollment_date')

        if birth_date and enrollment_date:
            if enrollment_date < birth_date:
                raise serializers.ValidationError({
                    'enrollment_date': 'Enrollment date cannot be before birth date.'
                })

            age_at_enrollment = (enrollment_date - birth_date).days / 365.25

            if age_at_enrollment < 10:
                raise serializers.ValidationError({
                    'enrollment_date': 'Student must be at least 10 years old at enrollment.'
                })

            if age_at_enrollment > 100:
                raise serializers.ValidationError({
                    'enrollment_date': 'Age at enrollment is unrealistic (more than 100 years).'
                })

        return data

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'document_number', 'document_type_id',
                  'birth_date', 'gender', 'student_number', 'enrollment_date', 'specialty_id',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
