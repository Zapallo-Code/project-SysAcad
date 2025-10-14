from rest_framework import serializers
from app.models.plan import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'start_date', 'end_date', 'observation']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=50, min_length=1)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    observation = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)

