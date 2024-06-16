from django.db import models  
from django.forms import fields  
from .models import post, Review, DiscountCodes
from django import forms  
from django.contrib.auth.forms import UserCreationForm
from registration.models import Profile

# class UserImage(models.Model):  
#     class Meta:  
#         # To specify the model to be used to create form  
#         model = post 
#         # It includes all the fields of model  
#         fields = '__all__'  

# class UserAddMoney(models.Model):

#     class Meta:
#         model = Profile
#         fields = ['cash', ]

class UserReview(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']

class AddDiscountCode( forms.ModelForm ):
    class Meta:
        model = DiscountCodes
        fields = ['title', 'discount']