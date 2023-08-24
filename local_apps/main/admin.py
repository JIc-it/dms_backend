from django.contrib import admin
from .models import UserSession

admin.site.site_header = 'DMS Admin'
admin.site.site_title = 'DMS Admin Panel'
admin.site.index_title = 'Welcome To DMS Admin Panel'


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'created_at']
    search_fields = ['user__email']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['user', 'session']

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
