import os
import datetime
from PIL import Image

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Profile(models.Model):

    def profile_pic_path(self, filename):
        if filename != settings.DEFAULT_PIC:
            base_filename, file_extension = os.path.splitext(filename)
            filename = (f'{self.user.username}{file_extension}')
            return f'post_pics/{filename}'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default=settings.DEFAULT_PIC, upload_to=profile_pic_path)
    date_Of_birth = models.DateField(null=True)
    address = models.TextField(null=True)    
    Gender = models.CharField(null='Male', max_length=10,
                              choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    
    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('profile')

    def save(self, *args, **kwargs):

        old_profile_pic = None
        if self.pk:
            old_profile_pic = Profile.objects.get(pk=self.pk).profile_pic
        
        super().save(*args, **kwargs)
        
        new_profile_pic = self.profile_pic
        if old_profile_pic != new_profile_pic:
            img = Image.open(self.profile_pic.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_pic.path)
