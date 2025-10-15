from rest_framework import serializers
from app.models.area import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=50, min_length=1)
