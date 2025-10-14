from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.specialty_type import SpecialtyType
from app.serializers.specialty_type_mapping import SpecialtyTypeSerializer
from app.services.specialty_type_service import SpecialtyTypeService


class SpecialtyTypeViewSet(viewsets.ModelViewSet):
    queryset = SpecialtyType.objects.all()
    serializer_class = SpecialtyTypeSerializer
    
    def list(self, request):
        tipos = SpecialtyTypeService.find_all()
        serializer = self.get_serializer(tipos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        tipo = SpecialtyTypeService.find_by_id(pk)
        if tipo is None:
            return Response(
                {'message': 'Specialty type not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(tipo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo = serializer.save()
            SpecialtyTypeService.create(tipo)
            return Response(
                'Tipo de specialty creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo = serializer.save()
            SpecialtyTypeService.update(pk, tipo)
            return Response(
                'Tipo de specialty actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        SpecialtyTypeService.delete_by_id(pk)
        return Response(
            'Tipo de specialty borrado exitosamente',
            status=status.HTTP_200_OK
        )
