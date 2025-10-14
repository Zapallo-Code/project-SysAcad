from rest_framework import serializers
from app.models.specialty import Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name', 'letter', 'observation', 'tipospecialty_id', 'faculty_id']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=100, min_length=1)
    letter = serializers.CharField(max_length=1, min_length=1)
    observation = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    tipospecialty_id = serializers.IntegerField()
    faculty_id = serializers.IntegerField()

