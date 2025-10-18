import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from app.serializers import PlanSerializer
from app.services import PlanService

logger = logging.getLogger(__name__)


class PlanViewSet(viewsets.ViewSet):
    serializer_class = PlanSerializer

    def list(self, request):
        try:
            planes = PlanService.find_all()
            serializer = self.serializer_class(planes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing plans: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            plan = PlanService.find_by_id(int(pk))
            if plan is None:
                return Response(
                    {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(plan)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving plan {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            plan = PlanService.create(serializer.validated_data)
            response_serializer = self.serializer_class(plan)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating plan: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_plan = PlanService.update(int(pk), serializer.validated_data)
            if updated_plan is None:
                return Response(
                    {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_plan)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            if "not found" in str(e).lower():
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating plan {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            plan = PlanService.find_by_id(int(pk))
            if plan is None:
                return Response(
                    {"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND
                )

            PlanService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting plan {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
