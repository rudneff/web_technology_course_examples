from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class CustomUser(User):
    avatar = models.ImageField()


# AUTH_USER_MODEL = 'myapp.MyUser'

# or

class Profile(models.Model):
    avatar = models.ImageField()
    user = models.OneToOneField(User)
