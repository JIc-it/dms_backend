from django.db import models
from local_apps.main.models import Main


class Company(Main):
    company_name = models.CharField(max_length=200)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company_name


class Department(Main):
    department_name = models.CharField(max_length=200)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department_name


class Designation(Main):
    designation_name = models.CharField(max_length=200)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'

    def __str__(self):
        return self.designation_name
