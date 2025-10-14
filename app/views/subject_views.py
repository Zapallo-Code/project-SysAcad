from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.subject import Subject
from app.serializers.subject_mapping import SubjectSerializer
from app.services.subject_service import SubjectService


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    
    def list(self, request):
        subjects = SubjectService.find_all()
        serializer = self.get_serializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        subject = SubjectService.find_by_id(pk)
        if subject is None:
            return Response(
                {'message': 'Subject not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(subject)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            SubjectService.create(subject)
            return Response(
                'Subject creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            subject = serializer.save()
            SubjectService.update(pk, subject)
            return Response(
                'Subject actualizada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        SubjectService.delete_by_id(pk)
        return Response(
            'Subject borrada exitosamente',
            status=status.HTTP_200_OK
        )
