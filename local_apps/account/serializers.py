from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source='company.company_name', read_only=True, allow_null=True)
    department = serializers.CharField(source='department.department_name', read_only=True, allow_null=True)
    designation = serializers.CharField(source='designation.designation_name', read_only=True, allow_null=True)
    reporting_manager = serializers.CharField(source='reporting_manager.email', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'account_id', 'first_name', 'last_name', 'email', 'mobile', 'company', 'department',
                  'designation', 'reporting_manager', 'date_of_joining']


class PasswordResetSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
