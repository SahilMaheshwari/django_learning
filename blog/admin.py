from django.contrib import admin
from .models import post, Cart, CartItems, Review, WishList, WishlistItems, DiscountCodes

admin.site.register(post)
admin.site.register(CartItems)
admin.site.register(Review)
admin.site.register(WishList)
admin.site.register(WishlistItems)
admin.site.register(DiscountCodes)
admin.site.register(Cart)