from rest_framework import viewsets, status
from rest_framework.response import Response
from app.models.document_type import DocumentType
from app.serializers.document_type_mapping import DocumentTypeSerializer
from app.services.document_type_service import DocumentTypeService


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
    
    def list(self, request):
        tipos = DocumentTypeService.find_all()
        serializer = self.get_serializer(tipos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        tipo = DocumentTypeService.find_by_id(pk)
        if tipo is None:
            return Response(
                {'message': 'Document type not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(tipo)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo = serializer.save()
            DocumentTypeService.create(tipo)
            return Response(
                'Tipo de documento creado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tipo = serializer.save()
            DocumentTypeService.update(pk, tipo)
            return Response(
                'Tipo de documento actualizado exitosamente',
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        DocumentTypeService.delete_by_id(pk)
        return Response(
            'Tipo de documento borrado exitosamente',
            status=status.HTTP_200_OK
        )
