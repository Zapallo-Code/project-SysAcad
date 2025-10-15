from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.university import University
from app.serializers.university import UniversitySerializer
from app.services.university import UniversityService


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    def list(self, request):
        universidades = UniversityService.find_all()
        serializer = self.get_serializer(universidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        university = UniversityService.find_by_id(pk)
        if university is None:
            return Response(
                {'message': 'University not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(university)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            university = serializer.save()
            UniversityService.create(university)
            return Response(
                'University creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            university = serializer.save()
            UniversityService.update(pk, university)
            return Response(
                'University actualizada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        UniversityService.delete_by_id(pk)
        return Response(
            'University borrada exitosamente',
            status=status.HTTP_200_OK
        )
