import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import SpecialtySerializer
from app.services import SpecialtyService

logger = logging.getLogger(__name__)


class SpecialtyViewSet(viewsets.ViewSet):
    serializer_class = SpecialtySerializer

    def list(self, request):
        try:
            specialties = SpecialtyService.find_all()
            serializer = self.serializer_class(specialties, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing specialties: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            specialty = SpecialtyService.find_by_id(int(pk))
            if specialty is None:
                return Response(
                    {'error': 'Specialty not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(specialty)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving specialty {pk}: {str(e)}")
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

            specialty = SpecialtyService.create(serializer.validated_data)
            response_serializer = self.serializer_class(specialty)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating specialty: {str(e)}")
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

            updated_specialty = SpecialtyService.update(int(pk), serializer.validated_data)
            if updated_specialty is None:
                return Response(
                    {'error': 'Specialty not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_specialty)
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
            logger.error(f"Error updating specialty {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        try:
            specialty = SpecialtyService.find_by_id(int(pk))
            if specialty is None:
                return Response(
                    {'error': 'Specialty not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            SpecialtyService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting specialty {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
