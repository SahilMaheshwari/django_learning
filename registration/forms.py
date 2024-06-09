from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    is_seller = forms.BooleanField(required=False)
    cash = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_seller', 'cash']
