from rest_framework import serializers
from app.models.university import University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'acronym']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=100, min_length=1)
    acronym = serializers.CharField(max_length=10, min_length=1)
