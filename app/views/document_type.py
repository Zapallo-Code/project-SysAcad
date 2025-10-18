import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import DocumentTypeSerializer
from app.services import DocumentTypeService

logger = logging.getLogger(__name__)


class DocumentTypeViewSet(viewsets.ViewSet):
    serializer_class = DocumentTypeSerializer

    def list(self, request):
        try:
            tipos = DocumentTypeService.find_all()
            serializer = self.serializer_class(tipos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing document types: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            tipo = DocumentTypeService.find_by_id(int(pk))
            if tipo is None:
                return Response(
                    {"error": "Document type not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(tipo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving document type {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            tipo = DocumentTypeService.create(serializer.validated_data)
            response_serializer = self.serializer_class(tipo)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating document type: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_tipo = DocumentTypeService.update(
                int(pk), serializer.validated_data
            )
            if updated_tipo is None:
                return Response(
                    {"error": "Document type not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            response_serializer = self.serializer_class(updated_tipo)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating document type {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            tipo = DocumentTypeService.find_by_id(int(pk))
            if tipo is None:
                return Response(
                    {"error": "Document type not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            DocumentTypeService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting document type {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
