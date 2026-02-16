from django.shortcuts import render

# Create your views here.


def login(request):
    context = {'title': 'Авторизация',
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