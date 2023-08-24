import django_filters
from .models import Document


class DocumentFilter(django_filters.FilterSet):
    company = django_filters.CharFilter(
        field_name='document_user__company__company_name',
        lookup_expr='in'
    )
    department = django_filters.CharFilter(
        field_name='document_user__department__department_name',
        lookup_expr='iexact'
    )
    shared_with = django_filters.CharFilter(
        field_name='shared_with__username',
        lookup_expr='iexact'
    )
    reporting_manager = django_filters.CharFilter(
        field_name='document_user__reporting_manager__username',
        lookup_expr='iexact'
    )

    class Meta:
        model = Document
        fields = []
