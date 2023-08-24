from django.contrib import admin
from .models import Document, DocumentVersion, DocumentCategory


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    pass


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    pass
