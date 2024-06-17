from django.urls import path
from . import views
from blog.views import add_to_cart, cart, placeorder, sellerhome, generate_report, add_to_wishlist, wishlist, delete_discount_code, seller, coupon_applied
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, review, DiscountListView, AddCode, SellerListView

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('about/', views.about, name = 'blog-about'),
    path('add-to-cart/<int:id>/<str:source>/', add_to_cart, name="add_to_cart"),
    path('cart/', cart, name="cart"),
    path('orderplaced/', placeorder, name="orderplaced"),
    path('sellerhome',sellerhome ,name = 'sellerhome'),
    path('generate-report',generate_report,name='generatereport'),
    path('post/<int:pk>/review', review.as_view() ,name='review'),
    path('add-to-wishlist/<int:id>/', add_to_wishlist, name="add_to_wishlist"),
    path('wishlist/', wishlist, name='wishlist'),
    path('post/<int:pk>/post_update', PostUpdateView.as_view(), name ='post_update'),
    path('discountcodes/', DiscountListView.as_view(), name='discountcodes'),
    path('delete-discount-code/<int:id>/',delete_discount_code,name='delete_discount_code'),
    path('add-discount-code', AddCode.as_view() ,name='add_discount_code'),
    path('sellers/', SellerListView.as_view(), name='sellers'),
    path('seller/<str:vendor>', seller, name='seller'),
    path('coupon_applied/', coupon_applied, name='coupon_applied')
]
  