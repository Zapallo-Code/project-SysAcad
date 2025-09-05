"""Forms for the Users app.

Includes:
- UserForm: create/update CustomUser with password handling and validation.
- StudentProfileForm: student profile data linked to a Career.
- ProfessorProfileForm: professor profile data.
- AdministratorProfileForm: administrator profile data.

Notes:
    Labels are in Spanish to match the current UI.
"""

from django import forms
from app.models import CustomUser, Student, Professor, Administrator, Career


class UserForm(forms.ModelForm):
    """
    Form to create or update a CustomUser with password management.

    Behavior:
        - On creation, password1 and password2 are required.
        - On update, passwords are optional; if provided, they must match.
        - Password is saved hashed via set_password() only when provided.

    Fields:
        username, first_name, last_name, email, dni, phone, birth_date,
        address, role, is_active (+ password1/password2 not in Meta).
    """
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput, strip=False, required=False)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput, strip=False, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'dni','phone', 'birth_date', 'address', 'role', 'is_active']

    def __init__(self, *args, **kwargs):
        """
        Initialize form and toggle password requirements based on instance state.

        If editing an existing user (instance.pk is set), passwords are optional.
        If creating a new user, passwords are required.
        """
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
        else:
            self.fields['password1'].required = True
            self.fields['password2'].required = True

    def clean(self):
        """
        Validate password fields according to create/update rules.

        - Create: both passwords required and must match.
        - Update: if either password is provided, both must be present and match.
        """
        cleaned = super().clean()
        pwd1 = cleaned.get("password1")
        pwd2 = cleaned.get("password2")

        if self.instance and self.instance.pk:
            if pwd1 or pwd2:
                if not pwd1:
                    self.add_error("password1", "Ingrese una contraseña.")
                if not pwd2:
                    self.add_error("password2", "Confirme la contraseña.")
                if pwd1 and pwd2 and pwd1 != pwd2:
                    self.add_error("password2", "Las contraseñas no coinciden.")
        else:
            if not pwd1 or not pwd2:
                self.add_error("password1", "Ingrese una contraseña.")
            elif pwd1 != pwd2:
                self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned

    def save(self, commit=True):
        """
        Persist the user and set a hashed password if provided.

        Args:
            commit (bool): Whether to save the instance to the DB. Defaults to True.

        Returns:
            CustomUser: The saved user instance.
        """
        user = super().save(commit=False)
        pwd = self.cleaned_data.get("password1")
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    """
    Form to edit student profile details.

    Fields:
        student_id, career, enrollment_date.
    """
    career = forms.ModelChoiceField(queryset=Career.objects.all(), label="Carrera")

    class Meta:
        model = Student
        fields = ['student_id', 'career', 'enrollment_date']
        labels = {'student_id': 'Legajo Estudiante', 'enrollment_date': 'Fecha de Ingreso'}


class ProfessorProfileForm(forms.ModelForm):
    """
    Form to edit professor profile details.

    Fields:
        professor_id, degree, category, hire_date.
    """
    class Meta:
        model = Professor
        fields = ['professor_id', 'degree', 'category', 'hire_date']
        labels = {'professor_id': 'Legajo Profesor', 'degree': 'Título', 'category': 'Categoría', 'hire_date': 'Fecha de Alta'}


class AdministratorProfileForm(forms.ModelForm):
    """
    Form to edit administrator profile details.

    Fields:
        administrator_id, position, hire_date.
    """
    class Meta:
        model = Administrator
        fields = ['administrator_id', 'position', 'hire_date']
        labels = {'administrator_id': 'Legajo Administrador', 'position': 'Cargo', 'hire_date': 'Fecha de Alta'}
