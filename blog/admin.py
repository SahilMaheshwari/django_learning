from django.contrib import admin
from .models import post, Cart, CartItems, Review

admin.site.register(post)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Review)