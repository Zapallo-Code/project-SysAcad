from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.department import Department
from app.serializers.department import DepartmentSerializer
from app.services.department import DepartmentService


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request):
        departments = DepartmentService.find_all()
        serializer = self.get_serializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        departament = DepartmentService.find_by_id(pk)
        if departament is None:
            return Response(
                {'message': 'Department not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(departament)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            departament = serializer.save()
            DepartmentService.create(departament)
            return Response(
                'Department creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            departament = serializer.save()
            DepartmentService.update(pk, departament)
            return Response(
                'Department actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        DepartmentService.delete_by_id(pk)
        return Response(
            'Department borrado exitosamente',
            status=status.HTTP_200_OK
        )
