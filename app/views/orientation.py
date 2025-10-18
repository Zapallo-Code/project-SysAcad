import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import OrientationSerializer
from app.services import OrientationService

logger = logging.getLogger(__name__)


class OrientationViewSet(viewsets.ViewSet):
    serializer_class = OrientationSerializer

    def list(self, request):
        try:
            orientations = OrientationService.find_all()
            serializer = self.serializer_class(orientations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing orientations: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            orientation = OrientationService.find_by_id(int(pk))
            if orientation is None:
                return Response(
                    {"error": "Orientation not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(orientation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving orientation {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            orientation = OrientationService.create(serializer.validated_data)
            response_serializer = self.serializer_class(orientation)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating orientation: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_orientation = OrientationService.update(
                int(pk), serializer.validated_data
            )
            if updated_orientation is None:
                return Response(
                    {"error": "Orientation not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_orientation)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating orientation {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            orientation = OrientationService.find_by_id(int(pk))
            if orientation is None:
                return Response(
                    {"error": "Orientation not found"}, status=status.HTTP_404_NOT_FOUND
                )

            OrientationService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting orientation {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
