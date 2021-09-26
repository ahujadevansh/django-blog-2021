from django import forms
from django.db.models import fields
from crispy_forms.helper import FormHelper
from tinymce import TinyMCE

from .models import Category, Post

class PostForm(forms.ModelForm):

    content = forms.CharField(
        widget=TinyMCE(attrs={
            'required': True,
            'cols': 30,
            'rows': 10
        }))

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'cover_pic']

class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add New Category'}))
    
    class Meta:
        model = Category
        fields = ['name']