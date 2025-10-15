from rest_framework import serializers
from app.models.position import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ['id', 'name', 'points', 'position_category_id', 'dedication_type_id']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=50, min_length=1)
    points = serializers.IntegerField(required=False, allow_null=True)
    position_category_id = serializers.IntegerField(write_only=True)
    dedication_type_id = serializers.IntegerField(write_only=True)
