from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.orientation import Orientation
from app.serializers.orientation import OrientationSerializer
from app.services.orientation import OrientationService


class OrientationViewSet(viewsets.ModelViewSet):
    queryset = Orientation.objects.all()
    serializer_class = OrientationSerializer

    def list(self, request):
        orientations = OrientationService.find_all()
        serializer = self.get_serializer(orientations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        orientacion = OrientationService.find_by_id(pk)
        if orientacion is None:
            return Response(
                {'message': 'Orientation not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(orientacion)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            orientacion = serializer.save()
            OrientationService.create(orientacion)
            return Response(
                'Orientación creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            orientacion = serializer.save()
            OrientationService.update(pk, orientacion)
            return Response(
                'Orientación actualizada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        OrientationService.delete_by_id(pk)
        return Response(
            'Orientación borrada exitosamente',
            status=status.HTTP_200_OK
        )
