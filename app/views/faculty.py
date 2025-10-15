from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.faculty import Faculty
from app.serializers.faculty import FacultySerializer
from app.services.faculty import FacultyService


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def list(self, request):
        faculties = FacultyService.find_all()
        serializer = self.get_serializer(faculties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        faculty = FacultyService.find_by_id(pk)
        if faculty is None:
            return Response(
                {'message': 'Faculty no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(faculty)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            faculty = serializer.save()
            FacultyService.create(faculty)
            return Response(
                'Faculty creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            faculty = serializer.save()
            FacultyService.update(pk, faculty)
            return Response(
                'Faculty actualizada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        FacultyService.delete_by_id(pk)
        return Response(
            'Faculty borrada exitosamente',
            status=status.HTTP_200_OK
        )
