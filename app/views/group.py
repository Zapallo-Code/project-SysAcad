from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.group import Group
from app.serializers.group import GroupSerializer
from app.services.group import GroupService


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def list(self, request):
        groups = GroupService.find_all()
        serializer = self.get_serializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        grupo = GroupService.find_by_id(pk)
        if grupo is None:
            return Response(
                {'message': 'Group not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(grupo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            grupo = serializer.save()
            GroupService.create(grupo)
            return Response(
                'Group creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            grupo = serializer.save()
            GroupService.update(pk, grupo)
            return Response(
                'Group actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        GroupService.delete_by_id(pk)
        return Response(
            'Group borrado exitosamente',
            status=status.HTTP_200_OK
        )
