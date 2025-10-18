import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import FacultySerializer
from app.services import FacultyService

logger = logging.getLogger(__name__)


class FacultyViewSet(viewsets.ViewSet):
    serializer_class = FacultySerializer

    def list(self, request):
        try:
            faculties = FacultyService.find_all()
            serializer = self.serializer_class(faculties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing faculties: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            faculty = FacultyService.find_by_id(int(pk))
            if faculty is None:
                return Response(
                    {"error": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(faculty)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving faculty {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            faculty = FacultyService.create(serializer.validated_data)
            response_serializer = self.serializer_class(faculty)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating faculty: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_faculty = FacultyService.update(int(pk), serializer.validated_data)
            if updated_faculty is None:
                return Response(
                    {"error": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_faculty)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating faculty {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            faculty = FacultyService.find_by_id(int(pk))
            if faculty is None:
                return Response(
                    {"error": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND
                )

            FacultyService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting faculty {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
