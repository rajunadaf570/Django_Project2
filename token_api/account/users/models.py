#python imports
import uuid

#django/rest_framework imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


#project level imports
from libs.models import TimeStampedModel

#third paty imports
from model_utils import Choices

# app level imports
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    mobile = models.BigIntegerField(unique=True,
        validators=[
            MinValueValidator(5000000000),
            MaxValueValidator(9999999999),
        ]
    )
    GENDER = Choices(
        ('M','Male'),
        ('F','Female'),
        ('O','Other')
    )

    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # is_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=5, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
    gender = models.CharField(choices=GENDER, max_length=1, blank=False)
    address = models.TextField(blank=False,default='')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        app_label = 'account'
        # db_table = 'api_user'

    @property
    def full_name(self):
        return "{fn} {ln}".format(fn=self.first_name, ln=self.last_name)

    @property
    def access_token(self):
        token, is_created = Token.objects.get_or_create(user=self)
        return token.key