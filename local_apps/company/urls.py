from django.urls import path
from .views import CompanyListView, DepartmentListView, DesignationListView

urlpatterns = [
    path('company-list', CompanyListView.as_view(), name='company-list'),
    path('department-list', DepartmentListView.as_view(), name='department-list'),
    path('designation-list', DesignationListView.as_view(), name='designation-list'),

]
