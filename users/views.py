from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate

from users.forms import UserLoginForm, UserRegisterForm, ProfileForm


# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                # Возвращаем пользователя
                auth.login(request, user)
                messages.success(request, f"Добро пожаловать! {username}")
                # Перенаправляем в профиль
                return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Авторизация',
        'form': form
    }
    return render(request, 'login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()  # сохраняем в бд
            # Перенаправляем в профиль
            user = form.instance
            auth.login(request, user)
            messages.success(request, "Регистрация прошла успешно.")
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = UserRegisterForm()

    context = {'title': 'Регистрация',
               'form': form}

    return render(request, 'registration.html', context)


@login_required(redirect_field_name='login')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():

            form.save()  # сохраняем в бд
            # Перенаправляем в профиль
            return HttpResponseRedirect(reverse("shop:catalogue"))
    else:
        # instance=request.user берем и передаем юзера в форму профиля
        form = ProfileForm(instance=request.user)

    context = {'title': 'Регистрация',
               'form': form}
    return render(request, 'profile.html', context)


@login_required
def logout(request):
    messages.success(request, f"{request.user.username} Пока-Пока!")
    auth.logout(request)
    return redirect(reverse("shop:catalogue"))
