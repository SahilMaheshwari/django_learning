from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from .models import post, Cart, CartItems, Review
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect   
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from registration.models import Profile
from .mailer import sendDaMail
import csv
from .forms import UserReview
from django.urls import reverse_lazy
from django.utils import timezone



# def home(request):
#     context = {
#         'posts' : post.objects.all()
#         }
#     return render(request, 'blog/home.html', context)
#     if request.method == 'POST':  
#         form = UserImage(request.POST, request.FILES)  
#         if form.is_valid():  
#             form.save()  
  
#             # Getting the current instance object to display in the template  
#             img_object = form.instance  
              
#             return render(request, 'blog/post_form.html', {'form': form, 'img_obj': img_object})  
#     else:  
#         form = UserImage()  
  
#     return render(request, 'blog/post_form.html', {'form': form})  

class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-orders']

    def as_seller(self, request):
        if request.user.profile.is_seller:
            self.template_name = 'blog/sellerhome.html'
        return self.as_view()


class PostDetailView(DetailView):
    model = post

class PostCreateView(CreateView):
    model = post
    fields = ['title', 'price', 'image', 'description', 'stock']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})

@login_required
def add_to_cart(request, id):
    product = post.objects.get(id=id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user = user, is_paid = False)
    if created:
        print("Created a new cart for the user")
    else:
        print("Existing cart found for the user")

    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = 1
        cart_item.save()
        print(f"Added {product} to cart {cart}")
    else:
        cart_item.quantity += 1
        cart_item.save()
        print(f"Updated {product} quantity in cart {cart}")
    return HttpResponseRedirect('/')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user = request.user, is_paid = False)
    cart_items = cart.cartitems_set.all()
    products = [i.product for i in cart_items]

    context = {
        'cart': cart,
        'cart_items': cart_items,  # Use the related_name 'items'
        'products': products
    }

    return render(request, 'blog/cart.html', context)

@login_required
def placeorder(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.filter(is_paid=False, user=user).first()
        profile = Profile.objects.filter(user=user).first()
        cart_items = cart.cartitems_set.all()
        stockenough = True

        for products in cart_items:
            if products.product.stock < products.quantity:
                stockenough = False

        if cart:
            if stockenough :
                if profile.cash > cart.total_price():
                    cart.is_paid = True
                    cart.date_placed = timezone.now()
                    cart.save()
                    profile.cash = profile.cash - cart.total_price()
                    profile.save()

                    for products in cart_items:
                        products.product.stock -= products.quantity
                        products.product.orders += products.quantity
                        products.product.save()
                        #sendDaMail(products.product.author.email, products.product.author.username, products.product.title, products.quantity)

                    return render(request, 'blog/orderplaced.html')
                else:
                    return render(request, 'blog/sorry.html', {'sorrytext' : "Not enough money in account"})
            else:
                cart.delete()
                return render(request, 'blog/sorry.html', {'sorrytext' : "Sorry, please order quantity in stock"})
        else:
            return redirect('cart')  # If no cart found, redirect to the cart page

    return redirect('cart')  # Redirect to cart if the request method is not POST

@login_required
def sellerhome(request):
    posts = post.objects.filter(author = request.user)
    return render(request, 'blog/sellerhome.html', {'posts' : posts})

@login_required
def orderhistory(request):
    user = request.user
    orders = Cart.objects.filter(is_paid=True, user=user).order_by('-id')

    return render(request, 'blog/orderhistory.html', {'orders' : orders})

@login_required
def generate_report(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=report.csv'

    writer = csv.writer(response)
    posts = post.objects.filter(author = request.user)
    writer.writerow(['Name', 'Cost/Unit', 'Orders', 'Inventory'])

    for i in posts:
        writer.writerow([i.title, i.price, i.orders, i.stock])

    return response

class review(CreateView):
    model = Review
    form_class = UserReview
    template_name = 'blog/review.html'

    def get_success_url(self):
        # Redirect to the detail view of the associated Post
        return reverse_lazy('post-detail', kwargs={'pk': self.object.product.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product_id = self.kwargs['pk']
        return super().form_valid(form)

