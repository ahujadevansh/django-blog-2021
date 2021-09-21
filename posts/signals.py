import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from .models import Post

@receiver(pre_save, sender=Post)
def post_cover_pic_delete_on_change(sender, instance, **kwargs):
    
    if not instance.pk:
        return False
    old_cover_pic = sender.objects.get(pk = instance.pk).cover_pic
    new_cover_pic = instance.cover_pic
    if old_cover_pic not in (new_cover_pic, settings.DEFAULT_PIC):
        if os.path.isfile(old_cover_pic.path):
            os.remove(old_cover_pic.path)

@receiver(post_delete, sender=Post)
def post_cover_pic_delete_on_change(sender, instance, **kwargs):
    
    cover_pic = instance.cover_pic
    if cover_pic.__str__() not in (settings.DEFAULT_PIC):
        if os.path.isfile(cover_pic.path):
            os.remove(cover_pic.path)




