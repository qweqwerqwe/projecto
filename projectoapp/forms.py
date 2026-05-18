from django.forms import ModelForm
from django import forms

from projectoapp.models import Institution, Project


class InstitutionForm(ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'
        labels = {
            'name': 'Наименование учебного заведения', 
            'address': 'Адрес'
        }


class StudentForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логин')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Пароль'
    )
    last_name = forms.CharField(max_length=20, label='Фамилия')
    first_name = forms.CharField(max_length=20, label='Имя')
    phone_number = forms.CharField(max_length=20, label='Номер телефона')
    institution_name = forms.CharField(max_length=50, label='Наименование учебного заведения')


class EmployerForm(forms.Form):
    username = forms.CharField(max_length=20, label='Логин')
    password = forms.CharField(
        widget=forms.PasswordInput, label='Пароль'
    )
    name = forms.CharField(max_length=50, label='Работадатель')
    address = forms.CharField(max_length=100, label='Адрес')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'discription', 'github_url']
        labels = {
            'name': 'Название проекта', 
            'discription': 'Описание', 
            'github_url': 'Ссылка на проект'
        }