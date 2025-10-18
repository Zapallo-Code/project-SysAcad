import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import PositionCategorySerializer
from app.services import PositionCategoryService

logger = logging.getLogger(__name__)


class PositionCategoryViewSet(viewsets.ViewSet):
    serializer_class = PositionCategorySerializer

    def list(self, request):
        try:
            categorias = PositionCategoryService.find_all()
            serializer = self.serializer_class(categorias, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing position categories: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            categoria = PositionCategoryService.find_by_id(int(pk))
            if categoria is None:
                return Response(
                    {"error": "Position category not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.serializer_class(categoria)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving position category {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            categoria = PositionCategoryService.create(serializer.validated_data)
            response_serializer = self.serializer_class(categoria)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating position category: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_categoria = PositionCategoryService.update(
                int(pk), serializer.validated_data
            )
            if updated_categoria is None:
                return Response(
                    {"error": "Position category not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            response_serializer = self.serializer_class(updated_categoria)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating position category {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            categoria = PositionCategoryService.find_by_id(int(pk))
            if categoria is None:
                return Response(
                    {"error": "Position category not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            PositionCategoryService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting position category {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
