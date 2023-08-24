from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DocumentVersion, Document
import json


@receiver(post_save, sender=Document)
def create_document_version(sender, instance, created, **kwargs):
    doc = DocumentVersion(is_delete=instance.is_delete,
                          document_id_count=instance.document_id_count,
                          document_id=instance.document_id,
                          document_user=instance.document_user,
                          document_name=instance.document_name,
                          version_count=instance.version_count,
                          version=instance.version,
                          document_category=instance.document_category,
                          specify_category=instance.specify_category,
                          document_number=instance.document_number,
                          document_expiry=instance.document_expiry,
                          place_of_issue=instance.place_of_issue,
                          converted_pdf=instance.converted_pdf,
                          size=instance.size)
    doc.save()
    doc.shared_with.set(instance.shared_with.all())
    doc.save()
