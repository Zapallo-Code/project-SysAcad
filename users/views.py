"""Views for Users app: admin, student, and professor workflows.

Includes:
- Admin: CRUD for users, faculties, careers, subjects, finals, and assignments.
- Student: dashboard, subject/final inscriptions, regular certificate.
- Professor: dashboard, grade management, final inscriptions.

Notes:
    - Access control via role-based predicates (is_admin/is_student/is_professor).
    - Uses messages framework for user feedback.
    - Keeps business rules minimal in views; core rules live in models/services.
"""

from io import BytesIO
from pathlib import Path

from docxtpl import DocxTemplate
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from academics.forms import CareerForm, FacultyForm, FinalExamForm, GradeForm, SubjectForm
from app.models import Career, Faculty, FinalExam, Grade, Subject, FinalExamInscription, SubjectInscription, CustomUser, Professor, Student
from users.forms import AdministratorProfileForm, ProfessorProfileForm, StudentProfileForm, UserForm


# --------- Admin Views -------
def is_admin(user):
    """Return True if the user is authenticated and has administrator role."""
    return user.is_authenticated and user.role == CustomUser.Role.ADMIN


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Render the admin dashboard.

    Returns:
        HttpResponse: Admin dashboard page.
    """
    return render(request, "users/admin_dashboard.html")


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """
    List all users.

    Returns:
        HttpResponse: Page with user queryset.
    """
    users = CustomUser.objects.all()
    return render(request, "users/user_list.html", {"users": users})


@login_required
@user_passes_test(is_admin)
def user_create(request):
    """
    Create a new user and optional role-specific profile.

    Behavior:
        - Determines selected role from POST.
        - Validates UserForm and the matching profile form.
        - Creates both inside an atomic transaction.

    Returns:
        HttpResponse: Redirect to list on success or form page on error.
    """
    selected_role = None
    if request.method == "POST":
        user_form = UserForm(request.POST)
        selected_role = request.POST.get("role")
        student_profile_form = StudentProfileForm(request.POST)
        professor_profile_form = ProfessorProfileForm(request.POST)
        administrator_profile_form = AdministratorProfileForm(request.POST)

        if selected_role == CustomUser.Role.STUDENT:
            profile_form = student_profile_form
        elif selected_role == CustomUser.Role.PROFESSOR:
            profile_form = professor_profile_form
        elif selected_role == CustomUser.Role.ADMIN:
            profile_form = administrator_profile_form
        else:
            profile_form = None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            with transaction.atomic():
                user = user_form.save()
                if profile_form is not None:
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("users:user-list")
    else:
        user_form = UserForm()
        student_profile_form = StudentProfileForm()
        professor_profile_form = ProfessorProfileForm()
        administrator_profile_form = AdministratorProfileForm()
    return render(request, "users/user_form.html", {
            "user_form": user_form,
            "student_profile_form": student_profile_form,
            "professor_profile_form": professor_profile_form,
            "administrator_profile_form": administrator_profile_form,
            "selected_role": selected_role})


@login_required
@user_passes_test(is_admin)
def user_edit(request, pk):
    """
    Update a user and its role-specific profile.

    Behavior:
        - Saves UserForm, swaps/creates/deletes related profile based on chosen role.
        - All operations are transactional.

    Args:
        pk (int): User primary key.

    Returns:
        HttpResponse: Redirect to list on success or form page on error.
    """
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            role = user_form.cleaned_data["role"]
            student_instance = (getattr(user, "student", None) if role == CustomUser.Role.STUDENT else None)
            professor_instance = (getattr(user, "professor", None) if role == CustomUser.Role.PROFESSOR else None)
            administrator_instance = (getattr(user, "administrator", None) if role == CustomUser.Role.ADMIN else None)

            student_profile_form = StudentProfileForm(request.POST, instance=student_instance)
            professor_profile_form = ProfessorProfileForm(request.POST, instance=professor_instance)
            administrator_profile_form = AdministratorProfileForm(request.POST, instance=administrator_instance)

            if role == CustomUser.Role.STUDENT:
                profile_form = student_profile_form
            elif role == CustomUser.Role.PROFESSOR:
                profile_form = professor_profile_form
            elif role == CustomUser.Role.ADMIN:
                profile_form = administrator_profile_form
            else:
                profile_form = None

            if profile_form is None or profile_form.is_valid():
                with transaction.atomic():
                    user = user_form.save()
                    if role != CustomUser.Role.STUDENT and getattr(
                        user, "student", None
                    ):
                        user.student.delete()
                    if role != CustomUser.Role.PROFESSOR and getattr(
                        user, "professor", None
                    ):
                        user.professor.delete()
                    if role != CustomUser.Role.ADMIN and getattr(
                        user, "administrator", None
                    ):
                        user.administrator.delete()
                    if profile_form is not None:
                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile.save()
                messages.success(request, "Usuario actualizado correctamente.")
                return redirect("users:user-list")

        posted_role = request.POST.get("role")
        student_profile_form = StudentProfileForm(request.POST)
        professor_profile_form = ProfessorProfileForm(request.POST)
        administrator_profile_form = AdministratorProfileForm(request.POST)
        return render(request, "users/user_form.html", {
                "user_form": user_form,
                "student_profile_form": student_profile_form,
                "professor_profile_form": professor_profile_form,
                "administrator_profile_form": administrator_profile_form,
                "selected_role": posted_role})
    else:
        user_form = UserForm(instance=user)
        student_profile_form = StudentProfileForm(instance=getattr(user, "student", None))
        professor_profile_form = ProfessorProfileForm(instance=getattr(user, "professor", None))
        administrator_profile_form = AdministratorProfileForm(instance=getattr(user, "administrator", None))
        return render(request, "users/user_form.html", {
                "user_form": user_form,
                "student_profile_form": student_profile_form,
                "professor_profile_form": professor_profile_form,
                "administrator_profile_form": administrator_profile_form,
                "selected_role": user.role})


@login_required
@user_passes_test(is_admin)
def user_delete(request, pk):
    """
    Delete a user after confirmation.

    Args:
        pk (int): User primary key.

    Returns:
        HttpResponse: Confirmation page (GET) or redirect (POST).
    """
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("users:user-list")
    return render(request, "users/confirm_delete.html", {"user": user})


@login_required
@user_passes_test(is_admin)
def faculty_list(request):
    """
    List faculties.

    Returns:
        HttpResponse: Page with faculties queryset.
    """
    faculties = Faculty.objects.all()
    return render(request, "users/faculty_list.html", {"faculties": faculties})


@login_required
@user_passes_test(is_admin)
def faculty_create(request):
    """
    Create a faculty.

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    if request.method == "POST":
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:faculty-list")
    else:
        form = FacultyForm()
    return render(request, "users/faculty_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def faculty_edit(request, code):
    """
    Edit a faculty.

    Args:
        code (str): Faculty code (PK).

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    faculty = get_object_or_404(Faculty, code=code)
    if request.method == "POST":
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            return redirect("users:faculty-list")
    else:
        form = FacultyForm(instance=faculty)
    return render(request, "users/faculty_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def faculty_delete(request, code):
    """
    Delete a faculty after confirmation.

    Args:
        code (str): Faculty code (PK).

    Returns:
        HttpResponse: Confirmation page (GET) or redirect (POST).
    """
    faculty = get_object_or_404(Faculty, code=code)
    if request.method == "POST":
        faculty.delete()
        return redirect("users:faculty-list")
    return render(request, "users/confirm_delete.html", {"object": faculty, "back": "users:faculty-list"})


@login_required
@user_passes_test(is_admin)
def career_list(request):
    """
    List careers.

    Returns:
        HttpResponse: Page with careers queryset.
    """
    careers = Career.objects.all()
    return render(request, "users/career_list.html", {"careers": careers})


@login_required
@user_passes_test(is_admin)
def career_create(request):
    """
    Create a career.

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    if request.method == "POST":
        form = CareerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:career-list")
    else:
        form = CareerForm()
    return render(request, "users/career_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def career_edit(request, code):
    """
    Edit a career.

    Args:
        code (str): Career code (PK).

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    career = get_object_or_404(Career, code=code)
    if request.method == "POST":
        form = CareerForm(request.POST, instance=career)
        if form.is_valid():
            form.save()
            return redirect("users:career-list")
    else:
        form = CareerForm(instance=career)
    return render(request, "users/career_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def career_delete(request, code):
    """
    Delete a career after confirmation.

    Args:
        code (str): Career code (PK).

    Returns:
        HttpResponse: Confirmation page (GET) or redirect (POST).
    """
    career = get_object_or_404(Career, code=code)
    if request.method == "POST":
        career.delete()
        return redirect("users:career-list")
    return render(request, "users/confirm_delete.html", {"object": career, "back": "users:career-list"})


@login_required
@user_passes_test(is_admin)
def subject_list(request):
    """
    List subjects.

    Returns:
        HttpResponse: Page with subjects queryset.
    """
    subjects = Subject.objects.select_related("career").all()
    return render(request, "users/subject_list.html", {"subjects": subjects})


@login_required
@user_passes_test(is_admin)
def subject_create(request):
    """
    Create a subject.

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:subject-list")
    else:
        form = SubjectForm()
    return render(request, "users/subject_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def subject_edit(request, code):
    """
    Edit a subject.

    Args:
        code (str): Subject code (PK).

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    subject = get_object_or_404(Subject, code=code)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect("users:subject-list")
    else:
        form = SubjectForm(instance=subject)
    return render(request, "users/subject_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def subject_delete(request, code):
    """
    Delete a subject after confirmation.

    Args:
        code (str): Subject code (PK).

    Returns:
        HttpResponse: Confirmation page (GET) or redirect (POST).
    """
    subject = get_object_or_404(Subject, code=code)
    if request.method == "POST":
        subject.delete()
        return redirect("users:subject-list")
    return render(request, "users/confirm_delete.html", {"object": subject, "back": "users:subject-list"})


@login_required
@user_passes_test(is_admin)
def assign_subject_professors(request, code):
    """
    Assign/remove professors for a subject.

    Args:
        code (str): Subject code (PK).

    Returns:
        HttpResponse: Redirect to list after processing or form page (GET).
    """
    subject = get_object_or_404(Subject, code=code)
    if request.method == "POST":
        # Professor primary key is a string (professor_id), keep as-is
        selected_ids = set(request.POST.getlist("professors"))
        current_ids = set(subject.professors.values_list("pk", flat=True))

        to_add = selected_ids - current_ids
        to_remove = current_ids - selected_ids

        if to_add or to_remove:
            with transaction.atomic():
                if to_add:
                    subject.professors.add(*to_add)
                if to_remove:
                    subject.professors.remove(*to_remove)
            messages.success(request, "Asignaciones actualizadas correctamente.")
        else:
            messages.info(request, "No hubo cambios en las asignaciones.")
        return redirect("users:subject-list")

    profs = Professor.objects.select_related("user").all()
    return render(request, "users/assign_professors.html", {"subject": subject, "professors": profs})


@login_required
@user_passes_test(is_admin)
def final_list(request):
    """
    List final exams.

    Returns:
        HttpResponse: Page with final exams queryset.
    """
    finals = FinalExam.objects.select_related("subject").all()
    return render(request, "users/final_list.html", {"finals": finals})


@login_required
@user_passes_test(is_admin)
def final_create(request):
    """
    Create a final exam.

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    if request.method == "POST":
        form = FinalExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:final-list")
    else:
        form = FinalExamForm()
    return render(request, "users/final_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def final_edit(request, pk):
    """
    Edit a final exam.

    Args:
        pk (int): FinalExam primary key.

    Returns:
        HttpResponse: Redirect on success or form page on error.
    """
    final = get_object_or_404(FinalExam, pk=pk)
    if request.method == "POST":
        form = FinalExamForm(request.POST, instance=final)
        if form.is_valid():
            form.save()
            return redirect("users:final-list")
    else:
        form = FinalExamForm(instance=final)
    return render(request, "users/final_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def final_delete(request, pk):
    """
    Delete a final exam after confirmation.

    Args:
        pk (int): FinalExam primary key.

    Returns:
        HttpResponse: Confirmation page (GET) or redirect (POST).
    """
    final = get_object_or_404(FinalExam, pk=pk)
    if request.method == "POST":
        final.delete()
        return redirect("users:final-list")
    return render(request, "users/confirm_delete.html", {"object": final, "back": "users:final-list"})


@login_required
@user_passes_test(is_admin)
def assign_final_professors(request, pk):
    """
    Assign/remove professors for a final exam.

    Args:
        pk (int): FinalExam primary key.

    Returns:
        HttpResponse: Redirect to list after processing or form page (GET).
    """
    final = get_object_or_404(FinalExam, pk=pk)
    if request.method == "POST":
        # Professor primary key is a string (professor_id), keep as-is
        selected_ids = set(request.POST.getlist("professors"))
        current_ids = set(final.professors.values_list("pk", flat=True))

        to_add = selected_ids - current_ids
        to_remove = current_ids - selected_ids

        if to_add or to_remove:
            with transaction.atomic():
                if to_add:
                    final.professors.add(*to_add)
                if to_remove:
                    final.professors.remove(*to_remove)
            messages.success(request, "Asignaciones del final actualizadas correctamente.")
        else:
            messages.info(request, "No hubo cambios en las asignaciones.")
        return redirect("users:final-list")

    profs = Professor.objects.select_related("user").all()
    return render(request, "users/assign_professors.html", {"final": final, "professors": profs})


# ------- Student Views -------
def is_student(user):
    """Return True if the user is authenticated and has student role."""
    return user.is_authenticated and user.role == CustomUser.Role.STUDENT


@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    """
    Render student dashboard with subjects, grades, and inscriptions.

    Context:
        subjects: Career subjects for the student.
        inscriptions: Subject inscriptions for the student.
        grades: Grade queryset for the student.
        eligible_finals: Finals where status is REGULAR.
        final_inscriptions: Final exam inscriptions.
        inscribed_final_ids: IDs of finals already inscribed.
        inscribed_subject_codes: Codes of subjects already inscribed.

    Returns:
        HttpResponse: Dashboard page.
    """
    student = getattr(request.user, "student", None)
    if not student:
        messages.error(request, "Tu perfil de estudiante no está configurado. Contactá a un administrador.")
        return redirect("home")
    subjects = Subject.objects.filter(career=student.career)
    inscriptions = SubjectInscription.objects.filter(student=student).select_related("subject")
    inscribed_subject_codes = list(inscriptions.values_list("subject__code", flat=True))
    grades = Grade.objects.filter(student=student).select_related("subject")

    eligible_subject_ids = (
        grades.filter(status=Grade.StatusSubject.REGULAR)
        .values_list("subject_id", flat=True)
        .distinct()
    )
    eligible_finals = FinalExam.objects.filter(subject_id__in=eligible_subject_ids)

    final_inscriptions = (
        FinalExamInscription.objects.filter(student=student)
        .select_related("final_exam__subject")
        .order_by("final_exam__date")
    )
    inscribed_final_ids = list(final_inscriptions.values_list("final_exam_id", flat=True))

    return render(request, "users/student_dashboard.html", {
            "subjects": subjects,
            "inscriptions": inscriptions,
            "grades": grades,
            "eligible_finals": eligible_finals,
            "final_inscriptions": final_inscriptions,
            "inscribed_final_ids": inscribed_final_ids,
            "inscribed_subject_codes": inscribed_subject_codes})


@login_required
@user_passes_test(is_student)
def subject_inscribe(request, subject_code):
    """
    Create subject inscription and ensure grade record exists.

    Args:
        subject_code (str): Subject code (PK).

    Returns:
        HttpResponse: Confirmation page (GET) or redirect (POST).
    """
    student = request.user.student
    subject = get_object_or_404(Subject, code=subject_code, career=student.career)
    if request.method == "POST":
        created = False
        obj, created = SubjectInscription.objects.get_or_create(student=student, subject=subject)
        Grade.objects.get_or_create(student=student, subject=subject)
        if created:
            messages.success(request, "Inscripción a la materia realizada.")
        else:
            messages.info(request, "Ya estabas inscripto en esta materia.")
        return redirect("users:student-dashboard")
    return render(request, "users/inscribe_confirm.html", {"subject": subject})


@login_required
@user_passes_test(is_student)
def final_exam_inscribe(request, final_exam_id):
    """
    Create final exam inscription if the subject status is REGULAR.

    Args:
        final_exam_id (int): FinalExam primary key.

    Returns:
        HttpResponse: Confirmation page (GET) or redirect (POST).
    """
    student = request.user.student
    final_exam = get_object_or_404(FinalExam, pk=final_exam_id, subject__career=student.career)
    grade = Grade.objects.filter(student=student, subject=final_exam.subject).order_by("-id").first()
    if not grade or grade.status not in [Grade.StatusSubject.REGULAR]:
        messages.error(request, "Solo puedes inscribirte si la materia está regular.")
        return redirect("users:student-dashboard")
    if request.method == "POST":
        FinalExamInscription.objects.get_or_create(student=student, final_exam=final_exam)
        messages.success(request, "Inscripción al final realizada.")
        return redirect("users:student-dashboard")
    return render(request, "users/inscribe_confirm.html", {"final_exam": final_exam})


@login_required
@user_passes_test(is_student)
def download_regular_certificate(request):
    """
    Generate and download a 'regular student' certificate as DOCX.
    """
    # Evitar acceder a request.user.student directamente (puede lanzar RelatedObjectDoesNotExist)
    user = request.user
    student = Student.objects.filter(user=user).select_related("career__faculty").first()
    if not student:
        messages.error(request, "Tu perfil de estudiante no está configurado. Contactá a un administrador.")
        return redirect("home")

    template_path = Path(settings.BASE_DIR) / "regular_certificate.docx"
    if not template_path.exists():
        messages.error(request, "No se encontró la plantilla de certificado.")
        return redirect("users:student-dashboard")

    today = timezone.localdate()
    context = {
        "full_name": request.user.get_full_name() or request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "dni": request.user.dni,
        "student_id": student.student_id,
        "career_name": student.career.name if student.career else "",
        "career_code": student.career.code if student.career else "",
        "faculty_name": (
            student.career.faculty.name
            if getattr(student, "career", None) and student.career and student.career.faculty
            else ""
        ),
        "enrollment_date": student.enrollment_date.strftime("%d/%m/%Y") if student.enrollment_date else "",
        "today_date": today.strftime("%d/%m/%Y"),
        "today_day": f"{today.day:02d}",
        "today_month": f"{today.month:02d}",
        "today_year": f"{today.year}",
    }

    try:
        doc = DocxTemplate(str(template_path))
        doc.render(context)
        output = BytesIO()
        doc.save(output)
        output.seek(0)
    except Exception:
        messages.error(request, "Ocurrió un error al generar el certificado.")
        return redirect("users:student-dashboard")

    filename = f"certificado-regular-{request.user.last_name or request.user.username}-{today.strftime('%Y%m%d')}.docx"
    response = HttpResponse(
        output.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response["Content-Disposition"] = f"attachment; filename=\"{filename}\""
    return response


# ------- Professor Views -------
def is_professor(user):
    """Return True if the user is authenticated and has professor role."""
    return user.is_authenticated and user.role == CustomUser.Role.PROFESSOR


@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    """
    Render professor dashboard with assigned subjects and finals.

    Returns:
        HttpResponse: Dashboard page.
    """
    professor = getattr(request.user, "professor", None)
    if not professor:
        messages.error(request, "Tu perfil de profesor no está configurado. Contactá a un administrador.")
        return redirect("home")
    subjects = professor.subjects.all()
    finals = professor.final_exams.select_related("subject").all()
    return render(request, "users/professor_dashboard.html", {"subjects": subjects, "finals": finals})


@login_required
@user_passes_test(is_professor)
def grade_list(request, subject_code):
    """
    List grades for a subject and backfill missing Grade entries.

    Args:
        subject_code (str): Subject code (PK) assigned to the professor.

    Returns:
        HttpResponse: Page with grades queryset.
    """
    professor = request.user.professor
    subject = get_object_or_404(Subject, code=subject_code, professors=professor)
    enrolled_student_ids = set(SubjectInscription.objects.filter(subject=subject).values_list("student_id", flat=True))
    existing_grade_student_ids = set(Grade.objects.filter(subject=subject).values_list("student_id", flat=True))
    missing_ids = enrolled_student_ids - existing_grade_student_ids
    if missing_ids:
        Grade.objects.bulk_create([Grade(student_id=sid, subject=subject) for sid in missing_ids])

    grades = (
        Grade.objects.filter(subject=subject)
        .select_related("student__user")
        .order_by("student__user__last_name", "student__user__first_name")
    )
    return render(request, "users/grade_list.html", {"grades": grades, "subject": subject})


@login_required
@user_passes_test(is_professor)
def grade_edit(request, pk):
    """
    Edit a grade record for a student in a professor's subject.

    Guards:
        - Professor must be assigned to the subject.
        - Student must be inscribed in the subject.

    Args:
        pk (int): Grade primary key.

    Returns:
        HttpResponse: Redirect to grade list on success or form page on error.
    """
    grade = get_object_or_404(Grade, pk=pk)
    if grade.subject not in request.user.professor.subjects.all():
        messages.error(request, "No puede editar notas de materias no asignadas.")
        return redirect("users:professor-dashboard")
    if not SubjectInscription.objects.filter(student=grade.student, subject=grade.subject).exists():
        messages.error(request, "Solo puede calificar a estudiantes inscriptos en la materia.")
        return redirect("users:grade-list", subject_code=grade.subject.code)

    if request.method == "POST":
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            status_was_changed = "status" in form.changed_data
            saved = form.save()
            if not status_was_changed:
                saved.update_status()
            return redirect("users:grade-list", subject_code=grade.subject.code)
    else:
        form = GradeForm(instance=grade)
    return render(request, "users/grade_form.html", {"form": form, "grade": grade})


@login_required
@user_passes_test(is_professor)
def professor_final_inscriptions(request, final_exam_id):
    """
    List final exam inscriptions assigned to the professor.

    Args:
        final_exam_id (int): FinalExam primary key.

    Returns:
        HttpResponse: Page with inscriptions queryset.
    """
    professor = request.user.professor
    final_exam = get_object_or_404(FinalExam, id=final_exam_id, professors=professor)
    inscriptions = (
        FinalExamInscription.objects.filter(final_exam=final_exam)
        .select_related("student__user")
        .order_by("student__user__last_name", "student__user__first_name")
    )
    return render(request, "users/professor_final_inscriptions.html", {
        "final_exam": final_exam, "inscriptions": inscriptions})
