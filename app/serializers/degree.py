from rest_framework import serializers
from app.models.degree import Degree


class DegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=50, min_length=1)
    description = serializers.CharField(max_length=200, min_length=1)
