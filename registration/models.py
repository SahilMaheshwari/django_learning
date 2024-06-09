from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_seller = models.BooleanField(default=False)
    cash = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Profile'
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
