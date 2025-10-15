from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import (
    UniversityViewSet,
    AreaViewSet,
    StudentViewSet,
    AuthorityViewSet,
    PositionViewSet,
    PositionCategoryViewSet,
    DepartmentViewSet,
    SpecialtyViewSet,
    FacultyViewSet,
    DegreeViewSet,
    GroupViewSet,
    SubjectViewSet,
    OrientationViewSet,
    PlanViewSet,
    DedicationTypeViewSet,
    DocumentTypeViewSet,
    SpecialtyTypeViewSet,
    HomeView,
)

router = DefaultRouter()
router.register(r'universidad', UniversityViewSet, basename='universidad')
router.register(r'area', AreaViewSet, basename='area')
router.register(r'alumno', StudentViewSet, basename='alumno')
router.register(r'authority', AuthorityViewSet, basename='authority')
router.register(r'cargo', PositionViewSet, basename='cargo')
router.register(r'categoriacargo', PositionCategoryViewSet, basename='categoriacargo')
router.register(r'departamento', DepartmentViewSet, basename='departamento')
router.register(r'especialidad', SpecialtyViewSet, basename='especialidad')
router.register(r'facultad', FacultyViewSet, basename='facultad')
router.register(r'grado', DegreeViewSet, basename='grado')
router.register(r'grupo', GroupViewSet, basename='grupo')
router.register(r'materia', SubjectViewSet, basename='materia')
router.register(r'orientacion', OrientationViewSet, basename='orientacion')
router.register(r'plan', PlanViewSet, basename='plan')
router.register(r'dedication_type', DedicationTypeViewSet, basename='dedication_type')
router.register(r'document_type', DocumentTypeViewSet, basename='document_type')
router.register(r'tipoespecialidad', SpecialtyTypeViewSet, basename='tipoespecialidad')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/v1/', include(router.urls)),
]
