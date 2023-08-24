import uuid
import shortuuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from local_apps.account.managers import CustomUserManager
from local_apps.company.models import Company, Designation, Department

ROLE = (
    ("Super_Admin", "Super Admin"),
    ("Admin", "Admin"),
    ('JIC-Staff', "JIC-Staff"),
    ("Others", "Others"),
)


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    is_email_verified = models.BooleanField(default=False)
    mobile = models.CharField(max_length=13, unique=True, blank=True, null=True,
                              error_messages={
                                  'unique': "A user with that mobile already exists.",
                              })
    is_mobile_verified = models.BooleanField(default=False)
    role = models.CharField(choices=ROLE, max_length=15, default='MD-Staff',
                            help_text='Id generation depends on the role. Once you submit it will be permanent.')
    is_first_time = models.BooleanField(default=True)
    company = models.ForeignKey(Company, related_name='document_version_company', on_delete=models.SET_NULL, blank=True,
                                null=True)
    department = models.ForeignKey(Department, related_name='document_version_department', on_delete=models.SET_NULL,
                                   blank=True, null=True)
    designation = models.ForeignKey(Designation, related_name='document_version_designation', on_delete=models.SET_NULL,
                                    blank=True, null=True)
    reporting_manager = models.ForeignKey('self', related_name='document_version_reporting_manager',
                                          on_delete=models.SET_NULL, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.account_id:
            if self.role == 'JIC-Staff':
                self.account_id = 'JIC-STF-' + shortuuid.ShortUUID().random(length=10)
            elif self.role == 'Admin':
                self.account_id = 'JIC-ADM-' + shortuuid.ShortUUID().random(length=10)
            elif self.role == 'Super_Admin':
                self.account_id = 'JIC-SUP-' + shortuuid.ShortUUID().random(length=10)
            else:
                self.account_id = 'JIC-OTR-' + shortuuid.ShortUUID().random(length=10)

        super(User, self).save(*args, **kwargs)
