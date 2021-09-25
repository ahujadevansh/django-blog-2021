import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

from .models import Profile

@receiver(post_save, sender=User)
def create_profile_on_user_create(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_delete, sender=Profile)
def user_profile_pic_delete_on_change(sender, instance, **kwargs):
    
    profile_pic = instance.profile_pic
    if profile_pic.__str__() not in (settings.DEFAULT_PIC):
        if os.path.isfile(profile_pic.path):
            os.remove(profile_pic.path)