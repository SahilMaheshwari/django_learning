from django.urls import path
from . import views
from blog.views import PostListView, PostDetailView, PostCreateView, add_to_cart, cart, placeorder, sellerhome

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('about/', views.about, name = 'blog-about'),
    path('add-to-cart/<int:id>/', add_to_cart, name="add_to_cart"),
    path('cart/', cart, name="cart"),
    path('orderplaced/', placeorder, name="orderplaced"),
    path('sellerhome',sellerhome ,name = 'sellerhome')
]
  