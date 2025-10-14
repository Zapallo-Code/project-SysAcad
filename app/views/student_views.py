from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.student import Student
from app.serializers.student_mapping import StudentSerializer
from app.services.student_service import StudentService


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def list(self, request):
        students = StudentService.find_all()
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        student = StudentService.find_by_id(pk)
        if student is None:
            return Response(
                {'message': 'Student not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            StudentService.create(student)
            return Response(
                'Student creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            StudentService.update(pk, student)
            return Response(
                'Student actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        StudentService.delete_by_id(pk)
        return Response(
            'Student borrado exitosamente',
            status=status.HTTP_200_OK
        )
