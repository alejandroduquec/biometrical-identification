"""Students forms."""

# Django
from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.utils import timezone

# Model
from django.contrib.auth.models import User
from students.models import Student, TypeFood, Institution

MONTH_CHOICES = [
    ('01', 'Enero'),
    ('02', 'Febrero'),
    ('03', 'Marzo'),
    ('04',  'Abril'),
    ('05', 'Mayo'),
    ('06', 'Junio'),
    ('07', 'Julio'),
    ('08', 'Agosto'),
    ('09', 'Septiembre'),
]


class RegisterStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'document',
            'document_type',
            'first_name',
            'last_name',
            'gender',
            'birthdate',
            'institution',
            'grade',
            'group',
            ]
        labels = {
            'document': 'Número de documento',
            'document_type': 'Tipo de documento',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'gender': 'Género',
            'birthdate': 'Fecha de nacimiento',
            'institution': 'Institución',
            'grade': 'Grado',
            'group': 'Grupo',
        }
        widgets = {
            'document': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'birthdate': forms.TextInput(attrs={'class': 'form-control', 'id': 'datepicker', 'data-inputmask': '"mask": "9999-99-99"', 'data-mask': 'true'}),
            'institution': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'group': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SearchStudentForm(forms.Form):
    """Search user Form."""

    student = forms.CharField(
        label='Búsqueda de Estudiante',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Nombre o Documento de identidad'
            }
        ))


class ReportPdfForm(forms.Form):
    """Report Pdf Form."""

    month = forms.CharField(
        label='Seleccione Mes',
        widget=forms.Select(
            choices=MONTH_CHOICES,
            attrs={
                'class': 'form-control',
            }
        )
    )

    institution = forms.ModelChoiceField(
        label='Seleccione institucion',
            queryset=Institution.objects.all(),
            widget=forms.Select(attrs={
                'class': 'form-control',
            })
        )
    type_food = forms.ModelChoiceField(
            label='Seleccione Tipo de Comida',
            queryset=TypeFood.objects.all(),
            widget=forms.Select(attrs={
                'class': 'form-control',
            })
        )


