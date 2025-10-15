from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.position_category import PositionCategory
from app.serializers.position_category import PositionCategorySerializer
from app.services.position_category import PositionCategoryService


class PositionCategoryViewSet(viewsets.ModelViewSet):
    queryset = PositionCategory.objects.all()
    serializer_class = PositionCategorySerializer

    def list(self, request):
        categorias = PositionCategoryService.find_all()
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        categoria = PositionCategoryService.find_by_id(pk)
        if categoria is None:
            return Response(
                {'message': 'Position category not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(categoria)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            PositionCategoryService.create(categoria)
            return Response(
                'Categoría de position creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            PositionCategoryService.update(pk, categoria)
            return Response(
                'Categoría de position actualizada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        PositionCategoryService.delete_by_id(pk)
        return Response(
            'Categoría de position borrada exitosamente',
            status=status.HTTP_200_OK
        )
