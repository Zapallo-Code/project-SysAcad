from rest_framework import serializers
from app.models.student import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'last_name', 'document_number', 'document_type_id', 
                  'birth_date', 'gender', 'student_id_number', 'enrollment_date', 'specialty_id']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=50, min_length=1)
    last_name = serializers.CharField(max_length=50, min_length=1)
    document_number = serializers.CharField(max_length=50, min_length=1)
    document_type_id = serializers.IntegerField()
    birth_date = serializers.DateField()
    gender = serializers.CharField(max_length=1, min_length=1)
    student_id_number = serializers.IntegerField()
    enrollment_date = serializers.DateField()
    specialty_id = serializers.IntegerField()
