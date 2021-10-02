import os
import datetime

from PIL import Image

from posts.managers import PostManager, CategoryManager
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Category(models.Model):
    
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(default='', editable=False, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(null=True, blank=True)
    objects = models.Manager()
    query = CategoryManager()

    def save(self, *args, **kwargs):
        value = slugify(self.name)
        self.slug = value
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        default_manager_name = "query"
        db_table = "posts_categories"
        verbose_name_plural = "Categories"

class Post(models.Model):

    def generate_cover_pic_path(self, filename):

        if filename != settings.DEFAULT_PIC:
            base_filename, file_extension = os.path.splitext(filename)
            current_time_str = datetime.datetime.now().strftime('%d-%m-%Y_%I:%M:%S,%f')
            filename = (f'{base_filename}_{current_time_str}{file_extension}')
            return f'post_pics/{filename}'

    title = models.CharField(max_length=250, unique=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(default='', editable=False, max_length=500)
    cover_pic = models.ImageField(default=settings.DEFAULT_PIC, upload_to=generate_cover_pic_path)
    views = models.BigIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateField(null=True, blank=True)
    objects = models.Manager()
    query = PostManager()

    def increment_views(self):
        self.views += 1
        self.save()

    def save(self, *args, **kwargs):
        value = slugify(self.title)
        self.slug = value
        old_cover_pic = None
        if self.id:
            old_cover_pic = Post.objects.get(id=self.id).cover_pic
        
        new_cover_pic = self.cover_pic
        super().save(*args, **kwargs)

        if old_cover_pic != new_cover_pic:
            cover_pic = Image.open(self.cover_pic.path)
            if cover_pic.height > 500 or cover_pic.width > 500:
                ouput_size = (500, 500)
                cover_pic.thumbnail(ouput_size)
                cover_pic.save(self.cover_pic.path)
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        default_manager_name = "query"
        db_table = "posts_posts"

# python manage.py makemigrations
# python manage.py migrate



