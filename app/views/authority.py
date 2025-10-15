from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.authority import Authority
from app.serializers.authority import AuthoritySerializer
from app.services.authority import AuthorityService


class AuthorityViewSet(viewsets.ModelViewSet):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer

    def list(self, request):
        authorities = AuthorityService.find_all()
        serializer = self.get_serializer(authorities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        authority = AuthorityService.find_by_id(pk)
        if authority is None:
            return Response(
                {'message': 'Authority no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(authority)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            authority = serializer.save()
            AuthorityService.create(authority)
            return Response(
                'Authority creada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            authority = serializer.save()
            AuthorityService.update(pk, authority)
            return Response(
                'Authority actualizada exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        AuthorityService.delete_by_id(pk)
        return Response(
            'Authority borrada exitosamente',
            status=status.HTTP_200_OK
        )
