from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export import resources
from .models import Department, Company, Designation


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = ['id', 'department_name']


@admin.register(Department)
class DepartmentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['department_name', 'created_at']
    search_fields = ['department_name']
    list_filter = ['created_at', 'updated_at']
    resource_class = DepartmentResource


class CompanyResource(resources.ModelResource):
    class Meta:
        model = Company
        fields = ['id', 'company_name']


@admin.register(Company)
class CompanyAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['company_name', 'created_at']
    search_fields = ['company_name']
    list_filter = ['created_at', 'updated_at']


class DesignationResource(resources.ModelResource):
    class Meta:
        model = Designation
        fields = ['id', 'designation_name']


@admin.register(Designation)
class DesignationAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['designation_name', 'created_at']
    search_fields = ['designation_name']
    list_filter = ['created_at', 'updated_at']
