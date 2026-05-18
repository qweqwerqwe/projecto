from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import generics
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import UserPassesTestMixin

from projectoapp.models import Employer, Institution, Project, Student
from projectoapp import forms


class AbstractListView(ListView):
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        student_id = self.request.GET.get('student_id')
        institution_id = self.request.GET.get('institution_id')

        context['has_filter'] = False

        if student_id:
            context['student'] = Student.objects.get(id=student_id)
            context['has_filter'] = True
        else:
            context['student'] = None

        if institution_id:
            context['institution'] = Institution.objects.get(id=institution_id)
            context['has_filter'] = True
        else:
            context['institution'] = None

        return context


class ProjectsListView(AbstractListView):
    model = Project
    template_name = 'projectslist.html'
    context_object_name = 'projects'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        student_id = self.request.GET.get('student_id')
        institution_id = self.request.GET.get('institution_id')

        if student_id:
            queryset.filter(student=student_id)
        elif institution_id:
            queryset.filter(student__institution=institution_id)

        return queryset.filter()


class StudentListView(AbstractListView):
    model = Student
    template_name = 'studentlist.html'
    context_object_name = 'students'

    def get_queryset(self):
        queryset = super().get_queryset()

        institution_id = self.request.GET.get('institution_id')

        if institution_id:
            queryset.filter(institution=institution_id)

        return queryset


class InstitutionListView(AbstractListView):
    model = Institution
    template_name = 'institutionlist.html'
    context_object_name = 'institutions'


class StudentFilterView(View):
    def get(self, request, id):
        student = Student.objects.get(id=id)

        if student is None:
            return redirect('projects')
        
        student_id = student.id
        institution_id = student.institution.id

        url = f"{reverse('projects')}?student_id={student_id}&institution_id={institution_id}"
        return redirect(url)
    

class InstitutionFilterView(View):
    def get(self, request, id):
        institution = Institution.objects.get(id=id)

        if institution is None:
            return redirect('projects')
        
        institution_id = institution.id

        url = f"{reverse('projects')}?institution_id={institution_id}"
        return redirect(url)
    

class StudentCreationView(View):
    def get(self, request):
        return render(request, 'registration/registration.html', {'form': forms.StudentForm()})
    

    def post(self, request):
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            institution = Institution.objects.get(name=form.cleaned_data['institution_name'])

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            user = User.objects.create_user(
                username=username, password=password, 
                last_name=last_name, first_name=first_name)
            
            user.groups.add(Group.objects.get(name='Students'))
            
            phone_number = form.cleaned_data['phone_number']
            
            Student.objects.create(user=user, institution=institution, phone_number=phone_number)

            return redirect('login')
        
        return render(request, 'registration/registration.html', {'form': form})
    

class InstitutionCreationView(View):
    def get(self, request):
        return render(request, 'institutionform.html', {'form': forms.InstitutionForm()})
    

    def post(self, request):
        form = forms.InstitutionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']

            Institution.objects.create(name=name, address=address)

            return redirect('projects')
        
        return render(request, 'institutionform.html', {'form': form})
    

class EmployerCreationView(View):
    def get(self, request):
        return render(request, 'registration/registration.html', {'form': forms.EmployerForm()})
    

    def post(self, request):
        form = forms.EmployerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create(username=username, password=password)
            user.groups.add(Group.objects.get(name='Employers'))

            name = form.cleaned_data['name']
            address = form.cleaned_data['address']

            Employer.objects.create(user=user, name=name, address=address)

            return redirect('login')
        
        return render(request, 'registration/registration.html', {'form': form})
    

class ProjectCreationView(UserPassesTestMixin, View):
    def get(self, request):
        return render(request, 'projectform.html', {'form': forms.ProjectForm()})
    

    def post(self, request):
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            discription = form.cleaned_data['discription']
            github_url = form.cleaned_data['github_url']

            student = Student.objects.get(user=request.user)

            Project.objects.create(name=name, discription=discription, 
                                student=student, github_url=github_url)

            return redirect('projects')
        
        return render(request, 'projectform.html', {'form': form})
    

    def test_func(self):
        return self.request.user.groups.filter(name='Students').exists()
    

    def handle_no_permission(self):
        return redirect('login')