from rest_framework import serializers
from app.models.authority import Authority


class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = ['id', 'name', 'phone', 'email', 'position_id']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=100, min_length=1)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    email = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    position_id = serializers.IntegerField()
