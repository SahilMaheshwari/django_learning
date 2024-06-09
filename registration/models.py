from django.db import models
from django.contrib.auth.models import User
from blog.models import post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_seller = models.BooleanField(default=False)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username} Profile'
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(post, on_delete=models.SET_NULL, null=True, blank=True)
    