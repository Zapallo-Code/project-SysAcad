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
        Generate certificate for a student in PDF, DOCX, ODT, or JSON format.
        Usage: GET /api/v1/student/{id}/certificate/?type=pdf|docx|odt|json
        """
        try:
            document_type = request.query_params.get("type", "pdf").lower()

            # Handle JSON format separately
            if document_type == "json":
                student = StudentService.find_by_id(int(pk))
                if not student:
                    return Response(
                        {"error": "Student not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Get full student data with relations
                from app.repositories import StudentRepository
                student_full = StudentRepository.find_with_full_relations(int(pk))
                
                certificate_data = {
                    "student": {
                        "id": student_full.id,
                        "first_name": student_full.first_name,
                        "last_name": student_full.last_name,
                        "full_name": f"{student_full.first_name} {student_full.last_name}",
                        "document_number": student_full.document_number,
                        "student_number": student_full.student_number,
                        "birth_date": str(student_full.birth_date),
                        "gender": student_full.gender,
                        "enrollment_date": str(student_full.enrollment_date),
                    },
                    "specialty": {
                        "id": student_full.specialty.id,
                        "name": student_full.specialty.name,
                        "letter": student_full.specialty.letter,
                    },
                    "faculty": {
                        "id": student_full.specialty.faculty.id,
                        "name": student_full.specialty.faculty.name,
                        "abbreviation": student_full.specialty.faculty.abbreviation,
                        "city": student_full.specialty.faculty.city,
                        "address": student_full.specialty.faculty.address,
                    },
                    "university": {
                        "id": student_full.specialty.faculty.university.id,
                        "name": student_full.specialty.faculty.university.name,
                        "acronym": student_full.specialty.faculty.university.acronym,
                    },
                    "certificate_date": StudentService._get_current_date(),
                }
                
                return Response(certificate_data, status=status.HTTP_200_OK)

            # Generate the certificate for document formats (PDF, DOCX, ODT)
            document_io = StudentService.generate_regular_student_certificate(
                int(pk), document_type
            )

            # Map document types to content types and file extensions
            content_type_map = {
                "pdf": "application/pdf",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "odt": "application/vnd.oasis.opendocument.text",
            }
            
            extension_map = {
                "pdf": "pdf",
                "docx": "docx",
                "odt": "odt",
            }

            content_type = content_type_map.get(document_type, "application/pdf")
            extension = extension_map.get(document_type, "pdf")

            # Return the document as a response
            response = HttpResponse(document_io.getvalue(), content_type=content_type)
            response["Content-Disposition"] = (
                f'attachment; filename="certificado_estudiante_{pk}.{extension}"'
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
