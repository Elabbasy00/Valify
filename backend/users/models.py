from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .managers import CustomUserManager


USERNAME_REGEX = r'^[\w.@+\-]+$'
# USERNAME_REGEX = r'^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$'  # (eg. Ahmed Elabbasy)


class User(AbstractUser):
    '''
        It's highly recommended to set up a custom user model when starting a new Django project. 
        to avoid links 
    '''
    username = models.CharField(max_length=150, unique=True, validators=[RegexValidator(
        regex=USERNAME_REGEX,  code='invalid_username')])

    email = models.EmailField(_('email address'), unique=True)

    public_key = models.TextField(null=True, blank=True)

    is_admin = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_short_name(self):
        ''' Keep short name for username as a slugFields in DRF '''
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


# class UserProfile(models.Model):
#     user = models.OneToOneField(
#         User, on_delete=models.CASCADE, related_name='profile')
#     public_key = models.TextField()

#     def __str__(self):
#         return "{} Profile".format(self.user.username)
