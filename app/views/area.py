import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import AreaSerializer
from app.services import AreaService

logger = logging.getLogger(__name__)


class AreaViewSet(viewsets.ViewSet):
    serializer_class = AreaSerializer

    def list(self, request):
        try:
            areas = AreaService.find_all()
            serializer = self.serializer_class(areas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing areas: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            area = AreaService.find_by_id(int(pk))
            if area is None:
                return Response(
                    {'error': 'Area not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(area)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving area {pk}: {str(e)}")
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

            area = AreaService.create(serializer.validated_data)
            response_serializer = self.serializer_class(area)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creating area: {str(e)}")
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

            updated_area = AreaService.update(int(pk), serializer.validated_data)
            if updated_area is None:
                return Response(
                    {'error': 'Area not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_area)
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
            logger.error(f"Error updating area {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        try:
            area = AreaService.find_by_id(int(pk))
            if area is None:
                return Response(
                    {'error': 'Area not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            AreaService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {'error': 'Invalid ID format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting area {pk}: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
