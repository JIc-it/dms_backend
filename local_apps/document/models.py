import shortuuid
from django.db import models
from local_apps.main.models import Main
from django.conf import settings
from local_apps.company.models import Department, Company, Designation


class DocumentCategory(Main):
    document_category_name = models.CharField(max_length=50, blank=True, null=True)
    have_multiple_pages = models.BooleanField(default=False)

    def __str__(self):
        return self.document_category_name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Document Category'
        verbose_name_plural = 'Document Categories'


class Document(Main):
    is_delete = models.BooleanField(default=False)
    document_id_count = models.IntegerField(default=0, blank=True, null=True)
    document_id = models.CharField(max_length=30, unique=True, blank=True, null=True)
    document_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='document_user',
                                      on_delete=models.SET_NULL, blank=True, null=True, )
    document_name = models.CharField(max_length=400, blank=True, null=True)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                         related_name='document_shared_with')
    version_count = models.IntegerField(default=0, blank=True, null=True)
    version = models.CharField(max_length=255, default='V1', blank=True, null=True)
    document_category = models.ForeignKey(DocumentCategory, related_name='document_document_category',
                                          on_delete=models.SET_NULL, blank=True, null=True)
    specify_category = models.CharField(max_length=12, blank=True, null=True)
    document_number = models.CharField(max_length=12, blank=True, null=True)
    document_expiry = models.DateField(blank=True, null=True)
    place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    converted_pdf = models.FileField(upload_to='document/converted_pdfs/', null=True, blank=True)
    size = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.document_id

    def save(self, *args, **kwargs):
        if self.converted_pdf:
            self.size = self.converted_pdf.size
        self.version_count = self.version_count + 1
        self.version = 'V' + str(self.version_count)
        if self.created_at == self.updated_at:
            last_emp_instance = Document.objects.order_by('-document_id_count').first()
            if last_emp_instance:
                self.document_id_count = last_emp_instance.document_id_count + 1
            else:
                self.document_id_count = 1
            self.document_id = 'JICDOC0000' + str(self.document_id_count)

        super().save(*args, **kwargs)


class DocumentVersion(Main):
    is_delete = models.BooleanField(default=False)
    document_id_count = models.IntegerField(default=0, blank=True, null=True)
    document_id = models.CharField(max_length=30, blank=True, null=True)
    document_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='document_version_user',
                                      on_delete=models.SET_NULL, blank=True, null=True, )
    document_name = models.CharField(max_length=400, blank=True, null=True)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                         related_name='document_version_shared_with')
    version_count = models.IntegerField(default=0, blank=True, null=True)
    version = models.CharField(max_length=255, default='V1', blank=True, null=True)
    document_category = models.ForeignKey(DocumentCategory, related_name='document_version_document_category',
                                          on_delete=models.SET_NULL, blank=True, null=True)
    specify_category = models.CharField(max_length=12, blank=True, null=True)
    document_number = models.CharField(max_length=12, blank=True, null=True)
    document_expiry = models.DateField(blank=True, null=True)
    place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    converted_pdf = models.FileField(upload_to='document_version/converted_pdfs/', null=True, blank=True)
    size = models.CharField(max_length=12, blank=True, null=True)  # bytes

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Document Version'
        verbose_name_plural = 'Document Versions'

    def __str__(self):
        return str(self.document_id) + ' - ' + str(self.version)
