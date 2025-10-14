from rest_framework import serializers
from app.models.department import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=50, min_length=1)

