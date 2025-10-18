import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


class HomeView(APIView):
    def get(self, request):
        try:
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in health check: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
