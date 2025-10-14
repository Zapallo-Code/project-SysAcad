from rest_framework import serializers
from app.models.position_category import PositionCategory


class PositionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionCategory
        fields = ['id', 'name']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=30, min_length=1)


