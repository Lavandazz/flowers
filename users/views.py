from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate

from users.forms import UserLoginForm, UserRegisterForm


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
            return HttpResponseRedirect(reverse("user:profile"))
    else:
        form = UserRegisterForm()
        print('Возвращаю обратно')

    context = {'title': 'Регистрация',
               'form': form}

    return render(request, 'registration.html', context)


def profile(request):
    context = {'title': 'Профиль',
    }
    return render(request, 'profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse("shop:catalogue"))
