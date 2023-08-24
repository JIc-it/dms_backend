from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from local_apps.emails.views import mail_handler


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    print('signal calling')
    data = {'email': instance.email if instance.email else "prince@jicitsolution.com"}
    subject = ''
    email_template = "emails/user_registration.html"
    mail_handler(mail_type='single', to=[str(instance.email)], subject=subject, data=data, template=email_template)
