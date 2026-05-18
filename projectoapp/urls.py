from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from projectoapp.views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'), 
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('projects/', ProjectsListView.as_view(), name='projects'), 
    path('students/', StudentListView.as_view(), name='students'), 
    path('institutions/', InstitutionListView.as_view(), name='institutions'), 
    path('students/<int:id>/', StudentFilterView.as_view(), name='students_filter'), 
    path('institutions/<int:id>/', InstitutionFilterView.as_view(), name='institutions_filter'), 
    path('student/', StudentCreationView.as_view(), name='student_form'), 
    path('institution/', InstitutionCreationView.as_view(), name='institution_form'), 
    path('employer/', EmployerCreationView.as_view(), name='employer_form'), 
    path('project/', ProjectCreationView.as_view(), name='project_form')
]