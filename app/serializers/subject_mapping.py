from rest_framework import serializers
from app.models.subject import Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'code', 'observation']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=255, min_length=1)
    code = serializers.CharField(max_length=20, min_length=1)
    observation = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
