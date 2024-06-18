from django.forms.models import BaseModelForm
from django.shortcuts import render
from django.http import HttpResponse
from .models import post, Cart, CartItems, Review, WishList, WishlistItems, DiscountCodes
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from registration.models import Profile
from .mailer import sendDaMail
import csv
from .forms import UserReview, AddDiscountCode
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User




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

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.is_seller:
            return redirect('sellerhome')
        return super().dispatch(request, *args, **kwargs)

class PostDetailView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'price', 'image', 'description', 'stock']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_seller:
            sellerhome(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = post
    fields = ['title', 'price', 'image', 'description', 'stock', 'discount']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_seller:
            sellerhome(request)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def about(request):
    return render(request, 'blog/about.html', {'title' : 'About'})

@login_required
def add_to_cart(request, id, source):
    product = post.objects.get(id=id)
    user = request.user
    cart, created = Cart.objects.get_or_create(user = user, is_paid = False)
    if created:
        print("Created a new cart for the user")
    else:
        print("Existing cart found for the user")

    
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)
    qty = int(request.POST.get('quantity', 1))
    if created:
        cart_item.quantity = qty
        cart_item.save()
        print(f"Added {product} to cart {cart}")
    else:
        cart_item.quantity += qty
        cart_item.save()
        print(f"Updated {product} quantity in cart {cart}")

    if source == 'wishlist':
        wishlist = WishList.objects.filter(user=user).first()
        wishlistitem = WishlistItems.objects.filter(wishlist=wishlist, product=product).first()
        wishlistitem.delete()

    return HttpResponseRedirect('/')

@login_required
def cart(request):
    if request.user.profile.is_seller:
        return render(request, 'blog/sellerhome.html')
    cart, created = Cart.objects.get_or_create(user = request.user, is_paid = False)
    cart_items = cart.cartitems_set.all()
    products = [i.product for i in cart_items]

    vendors = Profile.get_sellers()
    vendorsincart = [i.author.id for i in products]
    vendors = vendors.filter(user__id__in=vendorsincart)

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'products': products,
        'vendors': vendors
    }

    return render(request, 'blog/cart.html', context)

@login_required
def placeorder(request):
    if request.user.profile.is_seller:
        return render(request, 'blog/sellerhome.html')
    
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
                        try:
                            sendDaMail(products.product.author.email, products.product.author.username, products.product.title, products.quantity)
                        except:
                            print("mail wasnt sent")
                    return render(request, 'blog/orderplaced.html')
                else:
                    return render(request, 'blog/sorry.html', {'sorrytext' : "Not enough money in account"})
            else:
                cart.delete()
                return render(request, 'blog/sorry.html', {'sorrytext' : "Sorry, please order quantity in stock"})
        else:
            return redirect('cart')

    return redirect('cart')

@login_required
def sellerhome(request):
    posts = post.objects.filter(author = request.user)
    return render(request, 'blog/sellerhome.html', {'posts' : posts})

@login_required
def orderhistory(request):
    if request.user.profile.is_seller:
        return render(request, 'blog/sellerhome.html')
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
        return reverse_lazy('post-detail', kwargs={'pk': self.object.product.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product_id = self.kwargs['pk']
        return super().form_valid(form)

@login_required
def wishlist(request):

    if request.user.profile.is_seller:
        return render(request, 'blog/sellerhome.html')

    wish, created = WishList.objects.get_or_create(user = request.user)
    wish_items = wish.wishlistitems_set.all()
    products = [i.product for i in wish_items]

    context = {
        'wish': wish,
        'wish_items': wish_items,
        'products': products
    }

    return render(request, 'blog/wishlist.html', context)

@login_required
def add_to_wishlist(request, id):
    product = post.objects.get(id=id)
    user = request.user
    wish, created = WishList.objects.get_or_create(user = user)
    if created:
        print("Created a new WishList for the user")
    else:
        print("Existing WishList found for the user")

    wish_item, created = WishlistItems.objects.get_or_create(wishlist=wish, product=product)
    wish_item.save()
    print(f"Added {product} to WishList {wish}")

    return HttpResponseRedirect('/')

class DiscountListView(ListView):
    model = DiscountCodes
    template_name = 'blog/discountcodes.html'
    context_object_name = 'codes'
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.profile.is_seller:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        return DiscountCodes.objects.filter(author=user)

@login_required    
def delete_discount_code(request, id):
    code = get_object_or_404(DiscountCodes, id=id, author=request.user)
    code.delete()
    return redirect('discountcodes')  

class AddCode(CreateView):
    model = DiscountCodes
    form_class = AddDiscountCode
    template_name = 'blog/adddiscountcode.html'

    def get_success_url(self):
        return reverse_lazy('discountcodes')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class SellerListView(ListView):
    model = Profile
    template_name = 'blog/sellers.html'
    context_object_name = 'sellers'
    ordering = ['-id']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.is_seller:
            return redirect('sellerhome')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Profile.objects.filter(is_seller=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sellers = context['sellers']
        for seller in sellers:
            seller.listings_count = post.objects.filter(author=seller.user).count()
        return context
    
@login_required
def seller(request, vendor):
    author = User.objects.filter(username = vendor).first()
    posts = post.objects.filter(author = author.id)
    return render(request, 'blog/seller.html', {'posts' : posts})

@login_required
def coupon_applied(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code')    
        vendor = request.POST.get('vendor')

        codes = DiscountCodes.objects.filter(author = vendor)
        code_valid = codes.filter(title=discount_code).exists()

        if not code_valid:
            messages.error(request, f'Invalid code')
            return HttpResponseRedirect('/cart')

        cart = Cart.objects.filter(user = request.user, is_paid = False).first()
        discount_code_object = DiscountCodes.objects.filter(title = discount_code, author = vendor).first()
        codeexist = cart.add_coupon(discount_code_object)

        if not codeexist:
            messages.error(request, f'code applied already')
            return HttpResponseRedirect('/cart')
                
        cart = Cart.objects.filter(user = request.user, is_paid = False).first()
        cart_items = cart.cartitems_set.all()
        discount_object = DiscountCodes.objects.filter(title = discount_code).first()

        for i in cart_items:
            finaldisc = i.coupon_discount + discount_object.discount
            if finaldisc > 99:
                messages.error(request, "Discount limit reached")
            i.coupon_discount = finaldisc
            i.save()
        cart.price_saved()
        messages.success(request, "code applied")                        


    return HttpResponseRedirect('/cart')