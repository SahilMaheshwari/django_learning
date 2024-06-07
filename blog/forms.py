from django.db import models  
from django.forms import fields  
from .models import UploadImage, post  
from django import forms  
from django.contrib.auth.forms import UserCreationForm
  
  
class UserImage(models.Model):  
    class Meta:  
        # To specify the model to be used to create form  
        model = post 
        # It includes all the fields of model  
        fields = '__all__'  