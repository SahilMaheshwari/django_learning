from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from .models import post, Cart, CartItems
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect   
from django.http import HttpResponseRedirect
#from .forms import UserAddMoney
from django.contrib import messages


def home(request):
    context = {
        'posts' : post.objects.all()
        }
    return render(request, 'blog/home.html', context)
    if request.method == 'POST':  
        form = UserImage(request.POST, request.FILES)  
        if form.is_valid():  
            form.save()  
  
            # Getting the current instance object to display in the template  
            img_object = form.instance  
              
            return render(request, 'blog/post_form.html', {'form': form, 'img_obj': img_object})  
    else:  
        form = UserImage()  
  
    return render(request, 'blog/post_form.html', {'form': form})  

class PostListView(ListView):
    model = post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date']

class PostDetailView(DetailView):
    model = post

class PostCreateView(CreateView):
    model = post
    fields = ['title', 'price', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})

# def addmoney(request):
#     if request.method == 'POST':
#         form = UserAddMoney(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('profile')
#         else:
#             form = UserAddMoney()
#     return render(request, 'blog/addmoney.html', {'title' : 'Add Money'})

def add_to_cart(request, id):
    product = post.objects.get(id=id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user = user, is_paid = False)
    if created:
        print("Created a new cart for the user")
    else:
        print("Existing cart found for the user")

    cart_items = CartItems.objects.create(cart = cart, product = product)
    print(f"Added {product} to cart {cart}")
    return HttpResponseRedirect('/')

def cart(request):
    cart = Cart.objects.filter(is_paid = False, user = request.user)[0]
    cart_items = cart.cartitems_set.all()
    products = [i.product for i in cart_items]

    context = {
        'cart': cart,
        'cart_items': cart_items,  # Use the related_name 'items'
        'products': products
    }

    return render(request, 'blog/cart.html', context)