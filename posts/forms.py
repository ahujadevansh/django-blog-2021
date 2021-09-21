from django import forms

from tinymce import TinyMCE

from .models import Post

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