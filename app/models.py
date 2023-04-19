from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    test_field = models.CharField(max_length=3)


# class Profile(models.Model):
#     avatar = models.ImageField()
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#

