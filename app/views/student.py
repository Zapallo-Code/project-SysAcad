import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from app.serializers import StudentSerializer
from app.services import StudentService

logger = logging.getLogger(__name__)


class StudentViewSet(viewsets.ViewSet):
    serializer_class = StudentSerializer

    def list(self, request):
        try:
            students = StudentService.find_all()
            serializer = self.serializer_class(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error listing students: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        try:
            student = StudentService.find_by_id(int(pk))
            if student is None:
                return Response(
                    {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.serializer_class(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error retrieving student {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            student = StudentService.create(serializer.validated_data)
            response_serializer = self.serializer_class(student)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating student: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            updated_student = StudentService.update(int(pk), serializer.validated_data)
            if updated_student is None:
                return Response(
                    {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
                )

            response_serializer = self.serializer_class(updated_student)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating student {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None):
        try:
            student = StudentService.find_by_id(int(pk))
            if student is None:
                return Response(
                    {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
                )

            StudentService.delete_by_id(int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError:
            return Response(
                {"error": "Invalid ID format"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error deleting student {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"], url_path="certificate")
    def generate_certificate(self, request, pk=None):
        """
        Generate PDF certificate for a student.
        Usage: GET /api/v1/student/{id}/certificate/?type=pdf
        """
        try:
            document_type = request.query_params.get("type", "pdf").lower()

            # Generate the certificate
            pdf_io = StudentService.generate_regular_student_certificate(
                int(pk), document_type
            )

            # Return the PDF as a response
            response = HttpResponse(pdf_io.getvalue(), content_type="application/pdf")
            response["Content-Disposition"] = (
                f'attachment; filename="certificado_estudiante_{pk}.pdf"'
            )
            return response

        except ValueError as e:
            logger.error(f"Error generating certificate for student {pk}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error generating certificate for student {pk}: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
