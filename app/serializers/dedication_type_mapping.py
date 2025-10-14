from rest_framework import serializers
from app.models.dedication_type import DedicationType


class DedicationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DedicationType
        fields = ['id', 'name', 'observation']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=100, min_length=1)
    observation = serializers.CharField(max_length=200, min_length=1)

