from rest_framework import serializers
from app.models.orientation import Orientation


class OrientationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orientation
        fields = ['id', 'name', 'specialty_id', 'plan_id', 'subject_id']
        read_only_fields = ['id']

    name = serializers.CharField(max_length=50, min_length=1)
    specialty_id = serializers.IntegerField()
    plan_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
