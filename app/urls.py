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
router.register(r'university', UniversityViewSet, basename='university')
router.register(r'area', AreaViewSet, basename='area')
router.register(r'student', StudentViewSet, basename='student')
router.register(r'authority', AuthorityViewSet, basename='authority')
router.register(r'position', PositionViewSet, basename='position')
router.register(r'position_category', PositionCategoryViewSet, basename='position_category')
router.register(r'departament', DepartmentViewSet, basename='departament')
router.register(r'speciality', SpecialtyViewSet, basename='speciality')
router.register(r'faculty', FacultyViewSet, basename='faculty')
router.register(r'degree', DegreeViewSet, basename='degree')
router.register(r'group', GroupViewSet, basename='group')
router.register(r'subject', SubjectViewSet, basename='subject')
router.register(r'orientation', OrientationViewSet, basename='orientation')
router.register(r'plan', PlanViewSet, basename='plan')
router.register(r'dedication_type', DedicationTypeViewSet, basename='dedication_type')
router.register(r'document_type', DocumentTypeViewSet, basename='document_type')
router.register(r'speciality_type', SpecialtyTypeViewSet, basename='speciality_type')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/v1/', include(router.urls)),
]
