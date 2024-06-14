from django.contrib import admin
from .models import post, Cart, CartItems, Review, WishList, WishlistItems

admin.site.register(post)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Review)
admin.site.register(WishList)
admin.site.register(WishlistItems)