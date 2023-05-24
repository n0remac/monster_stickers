from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from monster_app.models import Monster

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    return render(request, 'login.html')

@login_required
def logout(request):
    return render(request, 'logout.html')

@login_required
def profile(request):
    monster_list = Monster.objects.filter(owner=request.user)
    return render(request, 'accounts/profile.html', {'monster_list': monster_list})