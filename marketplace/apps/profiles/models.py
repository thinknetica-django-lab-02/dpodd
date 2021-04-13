from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from sorl.thumbnail import ImageField

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    birthday = models.DateField(null=True)
    avatar = ImageField(upload_to='avatars', null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """Creates a Profile object for a new user."""
    profile, created = Profile.objects.get_or_create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def add_created_user_to_group(sender, instance, created, **kwargs):
    """Adds a newly created user to a "Common Users" group."""
    if created:
        instance.groups.add(Group.objects.get(name='common users'))
