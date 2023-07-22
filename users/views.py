from django.shortcuts import render, HttpResponseRedirect, redirect
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if user:
                auth.login(request, user)
                messages.success(request, f'Welcome, {user.username}!\nYou have successfully logged in.')
                return redirect('index')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered!')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile data has successfully changed!')
            return redirect('users:profile')
    form = UserProfileForm(instance=request.user)
    context = {'title': 'User profile', 'form': form}
    return render(request, 'users/profile.html', context)


def logout(request):
    username = request.user.username
    auth.logout(request)
    messages.success(request, f'Good by, {username}!\nYou have successfully logged out.')
    return redirect('index')
