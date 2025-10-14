from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.specialty import Specialty
from app.serializers.specialty_mapping import SpecialtySerializer
from app.services.specialty_service import SpecialtyService


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    
    def list(self, request):
        specialties = SpecialtyService.find_all()
        serializer = self.get_serializer(specialties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        specialty = SpecialtyService.find_by_id(pk)
        if specialty is None:
            return Response(
                {'message': 'Specialty not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(specialty)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            specialty = serializer.save()
            SpecialtyService.create(specialty)
            return Response(
                'Specialty creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            specialty = serializer.save()
            SpecialtyService.update(pk, specialty)
            return Response(
                'Specialty actualizada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        SpecialtyService.delete_by_id(pk)
        return Response(
            'Specialty borrada exitosamente',
            status=status.HTTP_200_OK
        )
