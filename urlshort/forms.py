from django.db import models
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ShortURL
from django import forms

class CreateNewShortURL(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = {'original_url'}
        widgets = {
            'original_url' : forms.TextInput(attrs={'class':'form-control'})
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        