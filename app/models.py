from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='avatar.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


