#python imports
import uuid

#django/rest_framework imports
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
# from django.contrib.postgres.fields.jsonb import JSONField as JSONBField


#project level imports
from libs.models import TimeStampedModel

#third paty imports
from model_utils import Choices
from jsonfield import JSONField

# app level imports
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    mobile = models.BigIntegerField(unique=True,
        validators = [
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
    is_email_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=60, blank=False)
    last_name = models.CharField(max_length=64, blank=False)
    email = models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
    gender = models.CharField(choices=GENDER, max_length=1, blank=False)
    address = models.TextField(blank=False,default='')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        app_label = 'account'
        verbose_name_plural = 'G-store'
        # db_table = 'api_user'

    @property
    def full_name(self):
        return "{fn} {ln}".format(fn=self.first_name, ln=self.last_name)

    @property
    def access_token(self):
        token, is_created = Token.objects.get_or_create(user=self)
        return token.key


class UserDetails(TimeStampedModel):
    '''
    '''
    mobile = models.BigIntegerField(
        validators=[
        MinValueValidator(5000000000),
        MaxValueValidator(9999999999),
        ],
        unique=True
    )
    name = models.CharField(default=False, max_length=65)
    email =models.EmailField(max_length=128, unique=True, db_index=True, blank=False)
    address = models.TextField(blank=True,default='')
    current_ctc = models.IntegerField(default=0)
    expected_ctc = models.IntegerField(default=0)
    notice_days = models.IntegerField(default=0)
    is_already_on_notice = models.BooleanField(default=False)
    experience = models.FloatField(default=0)
    tech_skills = JSONField(default={}, blank=True, null=True)
    preferable_locations = JSONField(default={}, blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user'
    )