from rest_framework import serializers
from .models import Document, DocumentCategory, DocumentVersion


class DocumentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentVersion
        fields = ['converted_pdf', 'created_at', 'size', 'version', 'document_expiry']


class DocumentSerializer(serializers.ModelSerializer):
    version_list = DocumentVersionSerializer(many=True, required=False, allow_null=True)
    document_category = serializers.CharField(source='document_category.document_category_name', read_only=True,
                                              allow_null=True)
    converted_pdf = serializers.FileField()

    class Meta:
        model = Document
        fields = ['id',
                  'converted_pdf',
                  'document_id',
                  'document_category',
                  'document_number',
                  'document_name',
                  'created_at',
                  'shared_with',
                  'size',
                  'version',
                  'shared_with',
                  'version',
                  'document_expiry',
                  'version_list']
        default = {
            'allow_null': True,
        }


class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ['id', 'document_category_name']
