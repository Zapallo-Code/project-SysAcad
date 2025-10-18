import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import AuthoritySerializer
from app.services import AuthorityService

logger = logging.getLogger(__name__)


class AuthorityViewSet(viewsets.ViewSet):
    serializer_class = AuthoritySerializer

    def list(self, request):
        try:
            authorities = AuthorityService.find_all()
            serializer = self.serializer_class(authorities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing authorities: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            authority = AuthorityService.find_by_id(int(pk))
            if authority is None:
                return Response(
                    {"error": "Authority not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(authority)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving authority {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            authority = AuthorityService.create(serializer.validated_data)
            response_serializer = self.serializer_class(authority)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating authority: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_authority = AuthorityService.update(
                int(pk), serializer.validated_data
            )
            if updated_authority is None:
                return Response(
                    {"error": "Authority not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_authority)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating authority {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            authority = AuthorityService.find_by_id(int(pk))
            if authority is None:
                return Response(
                    {"error": "Authority not found"}, status=status.HTTP_404_NOT_FOUND
                )

            AuthorityService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting authority {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
