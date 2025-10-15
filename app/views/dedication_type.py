from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.dedication_type import DedicationType
from app.serializers.dedication_type import DedicationTypeSerializer
from app.services.dedication_type import DedicationTypeService


class DedicationTypeViewSet(viewsets.ModelViewSet):
    queryset = DedicationType.objects.all()
    serializer_class = DedicationTypeSerializer

    def list(self, request):
        tipos = DedicationTypeService.find_all()
        serializer = self.get_serializer(tipos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        tipo = DedicationTypeService.find_by_id(pk)
        if tipo is None:
            return Response(
                {'message': 'Dedication type not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(tipo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo = serializer.save()
            DedicationTypeService.create(tipo)
            return Response(
                'Tipo de dedicación creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo = serializer.save()
            DedicationTypeService.update(pk, tipo)
            return Response(
                'Tipo de dedicación actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        DedicationTypeService.delete_by_id(pk)
        return Response(
            'Tipo de dedicación borrado exitosamente',
            status=status.HTTP_200_OK
        )
