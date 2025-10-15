from rest_framework import serializers
from app.models.group import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=50, min_length=1)
