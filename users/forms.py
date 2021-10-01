from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):

    email = forms.EmailField(label="Email Address")
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2',
        ]


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(label="Email Address")
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email',
        ]

class ProfileUpdateForm(forms.ModelForm):

    BIRTH_YEAR_CHOICES = range(1950,datetime.now().year +1)
    profile_pic = forms.ImageField(widget=forms.ClearableFileInput)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),input_formats=['%Y-%m-%d'],help_text='Format:YYYY-MM-DD')
    gender = forms.ChoiceField(widget=forms.RadioSelect,choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    class Meta:
        model = Profile
        fields = [
            'profile_pic', 'date_of_birth', 'address', 'gender'
        ]
