from rest_framework import serializers
from app.models.faculty import Faculty


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'abbreviation', 'directory', 'acronym', 'postal_code', 
                  'city', 'address', 'phone', 'contact_name', 'email', 'university_id']
        read_only_fields = ['id']
    
    name = serializers.CharField(max_length=100, min_length=1)
    abbreviation = serializers.CharField(max_length=10, min_length=1)
    directory = serializers.CharField(max_length=100, min_length=1)
    acronym = serializers.CharField(max_length=10, min_length=1)
    postal_code = serializers.CharField(max_length=10, required=False, allow_null=True, allow_blank=True)
    city = serializers.CharField(max_length=50, required=False, allow_null=True, allow_blank=True)
    address = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_null=True, allow_blank=True)
    contact_name = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    email = serializers.CharField(max_length=100, min_length=1)
    university_id = serializers.IntegerField()
