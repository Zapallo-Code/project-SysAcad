from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.degree import Degree
from app.serializers.degree import DegreeSerializer
from app.services.degree import DegreeService


class DegreeViewSet(viewsets.ModelViewSet):
    queryset = Degree.objects.all()
    serializer_class = DegreeSerializer

    def list(self, request):
        degrees = DegreeService.find_all()
        serializer = self.get_serializer(degrees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        degree = DegreeService.find_by_id(pk)
        if degree is None:
            return Response(
                {'message': 'Degree not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(degree)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            degree = serializer.save()
            DegreeService.create(degree)
            return Response(
                'Degree creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            degree = serializer.save()
            DegreeService.update(pk, degree)
            return Response(
                'Degree actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        DegreeService.delete_by_id(pk)
        return Response(
            'Degree borrado exitosamente',
            status=status.HTTP_200_OK
        )
