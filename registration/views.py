from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from blog.models import post
from .models import Profile

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            is_seller = form.cleaned_data.get('is_seller')
            cash = form.cleaned_data.get('cash')
            image = form.cleaned_data.get('image')
            userprofile = Profile.objects.filter(user=user).first()

            userprofile.is_seller = is_seller
            userprofile.cash = cash
            userprofile.image = image if image else 'default.jpg'
            userprofile.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()       
    return render(request, 'registration/register.html', {'form':form})

def user_logout(request):
    logout(request)
    return render(request, 'registration/logout.html', {})

@login_required
def profile(request):

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    if p_form.is_valid():
        p_form.save()
        messages.success(request, f'Account updated!')
        return redirect('profile')

    context = {'p_form' : p_form}

    return render(request, 'registration/profile.html', context)
