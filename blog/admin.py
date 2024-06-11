from django.contrib import admin
from .models import post, Cart, CartItems

admin.site.register(post)
admin.site.register(Cart)
admin.site.register(CartItems)