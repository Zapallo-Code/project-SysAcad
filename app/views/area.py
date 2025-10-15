from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.area import Area
from app.serializers.area import AreaSerializer
from app.services.area import AreaService


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def list(self, request):
        areas = AreaService.find_all()
        serializer = self.get_serializer(areas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        area = AreaService.find_by_id(pk)
        if area is None:
            return Response(
                {'message': 'Area not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(area)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            area = serializer.save()
            AreaService.create(area)
            return Response(
                'Area creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            area = serializer.save()
            updated_area = AreaService.update(pk, area)
            if updated_area is None:
                return Response(
                    {'message': 'Area not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                'Area actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        area = AreaService.find_by_id(pk)
        if area is None:
            return Response(
                {'message': 'Area not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        AreaService.delete_by_id(pk)
        return Response(
            'Area borrada exitosamente',
            status=status.HTTP_200_OK
        )
