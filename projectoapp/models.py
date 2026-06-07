from django.db import models
from django.contrib.auth.models import User


class Institution(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    address = models.CharField(max_length=100, null=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    institution = models.ForeignKey(Institution, null=False, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, unique=True, null=False)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=50, null=False, unique=True)
    address = models.CharField(max_length=100, null=True)


class Project(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    discription = models.CharField(max_length=300, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    github_url = models.CharField(max_length=300, null=False)


class Response(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, null=False)
    message = models.CharField(max_length=500, null=True)