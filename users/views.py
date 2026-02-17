from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate

from users.forms import UserLoginForm

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
    context = {'title': 'Регистрация',
    }
    return render(request, 'registration.html', context)


def profile(request):
    context = {'title': 'Профиль',
    }
    return render(request, 'profile.html', context)


def logout(request):
    context = {'title': 'Выход',
    }
    # return render(request, 'logout.html', context)