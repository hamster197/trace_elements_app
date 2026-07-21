from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email', unique=True, blank=False)

    first_name = models.CharField('First name', max_length=30, blank=False)
    last_name = models.CharField('Last Name', max_length=30, blank=False)
    patronymic = models.CharField('Middle name', max_length=45, blank=True)
    phone = models.CharField('Phone ', help_text='+7 *** *** ** **', max_length=12, blank=False)
    male = models.BooleanField('Male', default=False,)
    female = models.BooleanField('Female', default=False,)
    date_of_birth = models.DateField('Date of birth', )

    date_joined = models.DateTimeField('Date joined', auto_now_add=True)
    last_login = models.DateTimeField('Date last_login', auto_now=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Is_staff', default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']

    def clean(self,):
        if self.male == self.female:
            raise ValidationError('Choose one gender!')









