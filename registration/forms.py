from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_seller = forms.BooleanField(required=False)
    cash = forms.DecimalField(max_digits=10, decimal_places=2)
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','image', 'is_seller', 'cash']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['cash', ]

