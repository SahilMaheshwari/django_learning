from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_seller = models.BooleanField(default=False)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # latitude = models.DecimalField(default=28.658555)
    # longitude = models.DecimalField(default=77.189418)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_sellers():
        return Profile.objects.filter(is_seller=True)
