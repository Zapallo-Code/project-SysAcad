from rest_framework import serializers
from app.models.specialty_type import SpecialtyType


class SpecialtyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialtyType
        fields = ['id', 'name']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=50, min_length=1)
