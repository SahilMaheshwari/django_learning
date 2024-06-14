from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from registration.models import User

class post(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    orders = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default='No description given')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk})

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    date_placed = models.DateField(default=timezone.now)

    def total_price(self):
        cart_items = self.cartitems_set.all()
        cartPrice = sum(i.product.price*i.quantity for i in cart_items)
        return cartPrice

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(post, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    date_placed = models.DateField(default=timezone.now)

    def total_price(self):
        Wishlist_items = self.Wishlistitems_set.all()
        WishlistPrice = sum(i.product.price*i.quantity for i in Wishlist_items)
        return WishlistPrice

class WishlistItems(models.Model):
    Wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product = models.ForeignKey(post, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(post, on_delete=models.CASCADE, related_name="review")
    title = models.CharField(max_length=40, default='Review')
    content = models.CharField(max_length=200, default='No description given')
    rating = models.PositiveIntegerField(default=1)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s - %s' %(self.product.title, self.author)
    
