from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.position import Position
from app.serializers.position import PositionSerializer
from app.services.position import PositionService


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

    def list(self, request):
        positions = PositionService.find_all()
        serializer = self.get_serializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        position = PositionService.find_by_id(pk)
        if position is None:
            return Response(
                {'message': 'Position not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(position)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            position = serializer.save()
            PositionService.create(position)
            return Response(
                'Position creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            position = serializer.save()
            PositionService.update(pk, position)
            return Response(
                'Position actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        PositionService.delete_by_id(pk)
        return Response(
            'Position borrado exitosamente',
            status=status.HTTP_200_OK
        )
