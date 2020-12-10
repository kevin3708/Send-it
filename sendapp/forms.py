from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    location = forms.CharField(max_length=30,required=True)
    phone = forms.IntegerField()
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.' )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']