from rest_framework import generics
from .models import Company, Designation, Department
from .serializers import CompanySerializer, DesignationSerializer, DepartmentSerializer
from rest_framework.permissions import IsAuthenticated


class CompanyListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class DesignationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer


class DepartmentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
