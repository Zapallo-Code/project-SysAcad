import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import SpecialtyTypeSerializer
from app.services import SpecialtyTypeService

logger = logging.getLogger(__name__)


class SpecialtyTypeViewSet(viewsets.ViewSet):
    serializer_class = SpecialtyTypeSerializer

    def list(self, request):
        try:
            tipos = SpecialtyTypeService.find_all()
            serializer = self.serializer_class(tipos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing specialty types: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            tipo = SpecialtyTypeService.find_by_id(int(pk))
            if tipo is None:
                return Response(
                    {'error': 'Specialty type not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(tipo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving specialty type {pk}: {str(e)}")
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

            tipo = SpecialtyTypeService.create(serializer.validated_data)
            response_serializer = self.serializer_class(tipo)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating specialty type: {str(e)}")
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

            updated_tipo = SpecialtyTypeService.update(int(pk), serializer.validated_data)
            if updated_tipo is None:
                return Response(
                    {'error': 'Specialty type not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_tipo)
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
            logger.error(f"Error updating specialty type {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        try:
            tipo = SpecialtyTypeService.find_by_id(int(pk))
            if tipo is None:
                return Response(
                    {'error': 'Specialty type not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            SpecialtyTypeService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting specialty type {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
