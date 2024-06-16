from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from registration.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

class post(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    orders = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    description = models.CharField(max_length=200, default='No description given')
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(99)])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk' : self.pk})
    
    def is_discounted(self):
        if self.discount != 0:
            discountedprice = self.price * (100-self.discount) / 100
            return (True, discountedprice)
        return (False, self.price)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    date_placed = models.DateField(default=timezone.now)

    def total_price(self):
        cart_items = self.cartitems_set.all()
        cartPrice = 0
        for i in cart_items:
            is_discounted, discounted_price = i.product.is_discounted()
            if is_discounted:
                cartPrice += discounted_price*i.quantity
            else:
                cartPrice += i.product.price*i.quantity
        return cartPrice
    
    def price_saved(self):

        if self.total_price() == 0:
            print(0,0)
            return 0, 0

        cart_items = self.cartitems_set.all()
        original = sum(i.product.price*i.quantity for i in cart_items)
        discounted = self.total_price()
        saved = original - discounted
        percent = 100*(saved/original)

        print(saved, percent)
        return saved, percent

class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(post, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0)

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(post, on_delete=models.CASCADE, related_name="review")
    title = models.CharField(max_length=40, default='Review')
    content = models.CharField(max_length=200, default='No description given')
    rating = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(10)])
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return '%s - %s' %(self.product.title, self.author)
    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_placed = models.DateField(default=timezone.now)

    def total_price(self):
        Wishlist_items = self.wishlistitems_set.all()
        WishlistPrice = sum(i.product.price for i in Wishlist_items)
        return WishlistPrice

class WishlistItems(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(post, on_delete=models.SET_NULL, null=True, blank=True)
    
class DiscountCodes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(default='discount', max_length=8)
    discount = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(99)])
