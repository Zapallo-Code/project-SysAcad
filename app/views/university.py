import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import UniversitySerializer
from app.services import UniversityService

logger = logging.getLogger(__name__)


class UniversityViewSet(viewsets.ViewSet):
    serializer_class = UniversitySerializer

    def list(self, request):
        try:
            universities = UniversityService.find_all()
            serializer = self.serializer_class(universities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing universities: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            university = UniversityService.find_by_id(int(pk))
            if university is None:
                return Response(
                    {'error': 'University not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(university)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving university {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            university = UniversityService.create(serializer.validated_data)
            response_serializer = self.serializer_class(university)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating university: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            updated_university = UniversityService.update(int(pk), serializer.validated_data)
            if updated_university is None:
                return Response(
                    {'error': 'University not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_university)
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating university {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        try:
            university = UniversityService.find_by_id(int(pk))
            if university is None:
                return Response(
                    {'error': 'University not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            UniversityService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting university {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
