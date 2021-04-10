from django.db import models
from django.contrib.auth import get_user_model

from sorl.thumbnail import ImageField

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    birthday = models.DateField(null=True)
    avatar = ImageField(upload_to='avatars', null=True)
