from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import AddUserForm, UpdateUserForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UpdateUserForm
    add_form = AddUserForm

    list_display = (
        'account_id', 'first_name', 'last_name', 'email', 'is_email_verified', 'mobile', 'role', 'is_staff',
        'date_joined')
    list_filter = ('role', 'is_staff', 'is_email_verified')
    readonly_fields = ['account_id']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_email_verified', 'is_mobile_verified')}),
        ('Personal info', {'fields': ('account_id', 'first_name', 'last_name', 'mobile', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Company', {'fields': ('company', 'department', 'designation', 'reporting_manager', 'date_of_joining')}),

    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'first_name', 'last_name', 'email', 'mobile', 'role', 'password1', 'password2'
                )
            }
        ),
    )
    search_fields = ('account_id', 'first_name', 'last_name', 'email', 'mobile')
    ordering = ('first_name', 'last_name', 'email')
    filter_horizontal = ()
