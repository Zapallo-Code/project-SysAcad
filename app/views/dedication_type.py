import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import DedicationTypeSerializer
from app.services import DedicationTypeService

logger = logging.getLogger(__name__)


class DedicationTypeViewSet(viewsets.ViewSet):
    serializer_class = DedicationTypeSerializer

    def list(self, request):
        try:
            tipos = DedicationTypeService.find_all()
            serializer = self.serializer_class(tipos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing dedication types: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            tipo = DedicationTypeService.find_by_id(int(pk))
            if tipo is None:
                return Response(
                    {"error": "Dedication type not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(tipo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving dedication type {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            tipo = DedicationTypeService.create(serializer.validated_data)
            response_serializer = self.serializer_class(tipo)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating dedication type: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_tipo = DedicationTypeService.update(
                int(pk), serializer.validated_data
            )
            if updated_tipo is None:
                return Response(
                    {"error": "Dedication type not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            response_serializer = self.serializer_class(updated_tipo)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating dedication type {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            tipo = DedicationTypeService.find_by_id(int(pk))
            if tipo is None:
                return Response(
                    {"error": "Dedication type not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            DedicationTypeService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting dedication type {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
