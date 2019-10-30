# django imports
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, mobile, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given mobile number and password.
        AbstractBaseUser requires
        """
        print('hello-----------------------------------------')
        if not email:
            raise ValueError('Users must have a email')

        if not mobile:
            raise ValueError('Users must have a mobile')


        user = self.model(
            mobile=mobile,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password, **extra_fields):
        """
        Creates and saves a superuser with the given mobile number and password.
        """
        print('hey -----------------------------------------,----------')
        email = ""
        user = self.create_user(
            mobile,
            email,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
