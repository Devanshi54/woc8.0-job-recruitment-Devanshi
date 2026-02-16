from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm

from django.contrib.auth.decorators import login_required

def home(request):
    features = ['Jobs', 'Employers', 'Applications']
    return render(request, 'home.html', {'features': features})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.userprofile
    return render(request, 'profile.html', {'profile': profile})
from .forms import UserProfileForm

@login_required
def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})
@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'delete_confirm.html')

