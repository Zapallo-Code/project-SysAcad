import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import DegreeSerializer
from app.services import DegreeService

logger = logging.getLogger(__name__)


class DegreeViewSet(viewsets.ViewSet):
    serializer_class = DegreeSerializer

    def list(self, request):
        try:
            degrees = DegreeService.find_all()
            serializer = self.serializer_class(degrees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing degrees: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            degree = DegreeService.find_by_id(int(pk))
            if degree is None:
                return Response(
                    {"error": "Degree not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(degree)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving degree {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            degree = DegreeService.create(serializer.validated_data)
            response_serializer = self.serializer_class(degree)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating degree: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_degree = DegreeService.update(int(pk), serializer.validated_data)
            if updated_degree is None:
                return Response(
                    {"error": "Degree not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_degree)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating degree {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            degree = DegreeService.find_by_id(int(pk))
            if degree is None:
                return Response(
                    {"error": "Degree not found"}, status=status.HTTP_404_NOT_FOUND
                )

            DegreeService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting degree {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
